#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google files parser

Created on Fri Mar 22 11:59:29 2024

@author: IGOR POLEV
"""

import asyncio
from sys import argv as sys_argv

class GooGetFiles:
    
    def __init__(self, cmdl_params):
        pass
    
    async def run(self):
        pass

if __name__ == "__main__":
    script = GooGetFiles(sys_argv[1:])
    asyncio.run(script.run())
    