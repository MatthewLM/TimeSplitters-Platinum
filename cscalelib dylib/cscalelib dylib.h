/*
 *  cscalelib dylib.h
 *  cscalelib dylib
 *
 *  Created by Matthew Mitchell on 02/08/2010.
 *  Copyright 2010 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef cscalelib_dylib_
#define cscalelib_dylib_

/* The classes below are exported */
#pragma GCC visibility push(default)

class cscalelib_dylib
{
	public:
		void HelloWorld(const char *);
};

#pragma GCC visibility pop
#endif
