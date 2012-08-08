//
//  Application delegate.h
//  Scalelib Cocoa Framework
//
//  Created by Matthew Mitchell on 06/07/2010.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>


@protocol Application_delegate : NSApplicationDelegate

-(BOOL) applicationShouldTerminateAfterLastWindowClosed;

@end

