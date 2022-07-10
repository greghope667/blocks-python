import blocks
import unittest

def basic_block_1i1o():
    b = blocks.Node()
    i = blocks.InPort()
    o = blocks.OutPort()
    b.inputs["i"] = i
    b.outputs["o"] = o
    b.code = "o = i"
    return b


class TestBlocks(unittest.TestCase):

    def test_always(self):
        self.assertTrue(True)
    
    def test_create_basic_block(self):
        b = basic_block_1i1o()
        self.assertTrue(True)

    def test_basic_block_pass_value(self):
        b = basic_block_1i1o()
        b.inputs["i"].set(17)
        b.run()
        self.assertEqual(b.outputs["o"].get(), 17)
    
    def test_basic_block_throw(self):
        b = basic_block_1i1o()
        self.assertRaises(AssertionError, b.run)
        self.assertRaises(AssertionError, b.outputs["o"].get)
    
    def test_parse_error(self):
        b = basic_block_1i1o()
        b.inputs["i"].set(0)
        b.code = "o ====invalid==== i"
        b.run()
    
    def test_add(self):
        b = basic_block_1i1o()
        b.inputs["i2"] = blocks.InPort()
        b.code = "o = i + i2"
        b.inputs["i"].set(1)
        b.inputs["i2"].set(2)
        b.run()
        self.assertEqual(b.outputs["o"].get(), 3)
    
    def test_link(self):
        b1 = basic_block_1i1o()
        b2 = basic_block_1i1o()
        o = b1.outputs["o"]
        i = b2.inputs["i"]
        o.link(i)
        o.unlink(i)
    
    def test_null_pull(self):
        b = basic_block_1i1o()
        self.assertFalse(b.inputs["i"].try_pull())
    
    def test_link_pass_data(self):
        b1 = basic_block_1i1o()
        b2 = basic_block_1i1o()
        o = b1.outputs["o"]
        i = b2.inputs["i"]
        o.link(i)

        b1.inputs["i"].set(5)
        b1.run()
        i.try_pull()
        b2.run()
        self.assertEqual(b2.outputs["o"].get(), 5)
        
        
        

if __name__ == '__main__':
    unittest.main()
