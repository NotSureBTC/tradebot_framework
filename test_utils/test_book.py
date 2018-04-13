#!/usr/bin/env python2

import ExchgData
bfxdata = ExchgData.ExchgData('bfx')

bfxdata.update_book()
bfxdata.print_book()
print "now decay"
bfxdata.decay_book()
bfxdata.print_book()
print "now update"
bfxdata.update_book()
bfxdata.print_book()
