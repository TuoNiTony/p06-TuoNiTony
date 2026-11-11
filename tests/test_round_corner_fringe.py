# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

# Issue #2: transparent round_corner draws a dark ring. The arc pixels stay
# fully opaque, so no pixel on the arc is partly transparent. This test asks
# for at least one partly transparent pixel on the arc. It fails on the
# current code and should pass once the edge is smoothed through alpha.

from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerFringeTestCase(FilterTestCase):
    @gen_test
    async def test_round_corner_arc_has_partial_alpha(self):
        image = await self.get_filtered(
            "source.jpg",
            "thumbor.filters.round_corner",
            "round_corner(60,255,255,255,1)",
            mode="RGBA",
        )
        radius = 60
        partial = 0
        for y in range(radius):
            for x in range(radius):
                # distance from the arc centre (radius, radius)
                d = (
                    (radius - x - 0.5) ** 2 + (radius - y - 0.5) ** 2
                ) ** 0.5
                if radius - 1.5 <= d <= radius - 0.5:
                    alpha = image.getpixel((x, y))[3]
                    if 0 < alpha < 255:
                        partial += 1

        assert partial > 0, "no partly transparent pixel on the arc"
