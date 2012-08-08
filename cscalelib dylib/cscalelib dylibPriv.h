/*
 *  cscalelib dylibPriv.h
 *  cscalelib dylib
 *
 *  Created by Matthew Mitchell on 02/08/2010.
 *  Copyright 2010 __MyCompanyName__. All rights reserved.
 *
 */

/* The classes below are not exported */
#pragma GCC visibility push(hidden)

class cscalelib_dylibPriv
{
	public:
		void HelloWorldPriv(const char *);
};

#pragma GCC visibility pop
