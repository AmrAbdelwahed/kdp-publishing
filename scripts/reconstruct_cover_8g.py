"""Run Real-ESRGAN x4plus on CPU in context-padded tiles; no interpolation.

Requires numpy, Pillow and ncnn, plus the official x4plus .param/.bin files.
The model may hallucinate detail; output requires visual and rights review.
"""
import argparse
import time
from pathlib import Path
import ncnn
import numpy as np
from PIL import Image


def reconstruct(source, destination, model_dir, tile_size=192, context=32, threads=4):
    source=Path(source);destination=Path(destination);model_dir=Path(model_dir)
    if destination.exists():raise FileExistsError(f'Refusing to overwrite {destination}')
    if tile_size<1 or context<0 or threads<1:raise ValueError('Invalid tile, context or thread count')
    net=ncnn.Net();net.opt.use_vulkan_compute=False;net.opt.num_threads=threads
    for filename,loader in [('realesrgan-x4plus.param',net.load_param),('realesrgan-x4plus.bin',net.load_model)]:
        if loader(str(model_dir/filename))!=0:raise RuntimeError(f'Cannot load {filename}')
    with Image.open(source) as im: image=im.convert('RGB')
    width,height=image.size;result=Image.new('RGB',(width*4,height*4));total=((width+tile_size-1)//tile_size)*((height+tile_size-1)//tile_size)
    t=time.monotonic();n=0
    for y in range(0,height,tile_size):
        for x in range(0,width,tile_size):
            x1=min(x+tile_size,width);y1=min(y+tile_size,height)
            ax=max(0,x-context);ay=max(0,y-context);bx=min(width,x1+context);by=min(height,y1+context)
            pixels=np.asarray(image.crop((ax,ay,bx,by)),dtype=np.float32).transpose(2,0,1).copy()/255
            ex=net.create_extractor()
            if ex.input('data',ncnn.Mat(pixels))!=0:raise RuntimeError('Model input failed')
            status,mat=ex.extract('output')
            if status!=0:raise RuntimeError(f'Model inference failed for tile {x},{y}')
            output=np.asarray(mat)
            if output.shape!=(3,(by-ay)*4,(bx-ax)*4):raise ValueError(f'Unexpected output shape {output.shape}')
            core=output[:,(y-ay)*4:(y1-ay)*4,(x-ax)*4:(x1-ax)*4]
            rgb=np.uint8(np.clip(core.transpose(1,2,0)*255,0,255))
            result.paste(Image.fromarray(rgb,'RGB'),(x*4,y*4));del ex,mat,output,core,pixels,rgb
            n+=1;print(f'{n}/{total} tiles, {time.monotonic()-t:.1f}s',flush=True)
    destination.parent.mkdir(parents=True,exist_ok=True)
    result.save(destination,format='PNG',compress_level=6)
    print(f'Saved {destination}: {result.size}; {time.monotonic()-t:.1f}s',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source');p.add_argument('destination');p.add_argument('--model-dir',required=True)
    p.add_argument('--tile-size',type=int,default=192);p.add_argument('--context',type=int,default=32);p.add_argument('--threads',type=int,default=4)
    a=p.parse_args();reconstruct(a.source,a.destination,a.model_dir,a.tile_size,a.context,a.threads)
