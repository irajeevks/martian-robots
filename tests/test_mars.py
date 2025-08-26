import unittest
from mars import Grid, Robot, simulate, parse_input, format_output

class TestMars(unittest.TestCase):
    def test_turning(self):
        g = Grid(5,5)
        r = Robot(0,0,'N')
        r.turn_right(); self.assertEqual(r.orient, 'E')
        r.turn_right(); self.assertEqual(r.orient, 'S')
        r.turn_left();  self.assertEqual(r.orient, 'E')
        r.turn_left();  self.assertEqual(r.orient, 'N')

    def test_forward_within_bounds(self):
        g = Grid(2,2)
        r = Robot(1,1,'N')
        r.forward(g); self.assertEqual((r.x, r.y, r.orient, r.lost), (1,2,'N',False))
        r.turn_right()
        r.forward(g); self.assertEqual((r.x, r.y, r.orient, r.lost), (2,2,'E',False))

    def test_lost_and_scent(self):
        g = Grid(1,1)
        # First robot goes off from (1,1) heading N -> lost, scent at (1,1)
        r1 = simulate(g, (1,1,'N'), 'F')
        self.assertTrue(r1.lost)
        self.assertIn((1,1), g.scents)

        # Second robot at (1,1) heading N: forward would be off, but scented -> ignore, not lost
        r2 = simulate(g, (1,1,'N'), 'F')
        self.assertFalse(r2.lost)
        self.assertEqual((r2.x, r2.y, r2.orient), (1,1,'N'))

    def test_parse_and_sample(self):
        sample = [
            '5 3',
            '1 1 E',
            'RFRFRFRF',
            '',
            '3 2 N',
            'FRRFLLFFRRFLL',
            '',
            '0 3 W',
            'LLFFFLFLFL'
        ]
        grid, jobs = parse_input(sample)
        self.assertEqual((grid.max_x, grid.max_y), (5,3))
        outs = []
        for start, prog in jobs:
            outs.append(format_output(simulate(grid, start, prog)))
        self.assertEqual(outs, ['1 1 E', '3 3 N LOST', '2 3 S'])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            Grid(-1, 0)
        with self.assertRaises(ValueError):
            Grid(51, 0)  # over max constraint

        # Bad grid
        with self.assertRaises(ValueError):
            parse_input(['foo bar'])

        # Missing instruction
        with self.assertRaises(ValueError):
            parse_input(['1 1', '0 0 N'])

        # Bad command
        with self.assertRaises(ValueError):
            parse_input(['1 1', '0 0 N', 'FX'])

if __name__ == '__main__':
    unittest.main()
