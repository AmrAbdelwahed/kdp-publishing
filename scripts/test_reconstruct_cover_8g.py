"""Test tile coordinates, context cropping and overwrite safety, without model weights."""
import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

class FakeExtractor:
    def input(self,name,value):self.array=np.asarray(value);return 0
    def extract(self,name):return 0,np.repeat(np.repeat(self.array,4,axis=1),4,axis=2)
class FakeNet:
    def __init__(self):self.opt=types.SimpleNamespace()
    def load_param(self,path):return 0
    def load_model(self,path):return 0
    def create_extractor(self):return FakeExtractor()

class ReconstructionTilingTest(unittest.TestCase):
    def test_tiles_and_overwrite(self):
        fake=types.SimpleNamespace(Net=FakeNet,Mat=lambda array:array)
        spec=importlib.util.spec_from_file_location('cover_8g_test',ROOT/'scripts/reconstruct_cover_8g.py')
        module=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,{'ncnn':fake}):spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as t:
            folder=Path(t);src=folder/'src.png';dest=folder/'dest.png'
            original=np.arange(7*9*3,dtype=np.uint8).reshape((7,9,3))
            Image.fromarray(original).save(src)
            module.reconstruct(src,dest,folder,tile_size=3,context=2,threads=1)
            with Image.open(dest) as im:out=np.asarray(im)
            # Numeric roundoff in float conversion is at most one level.
            expected=np.repeat(np.repeat(original,4,axis=0),4,axis=1)
            self.assertLessEqual(np.abs(out.astype('int16')-expected.astype('int16')).max(),1)
            with self.assertRaises(FileExistsError):module.reconstruct(src,dest,folder)

if __name__=='__main__':unittest.main()
