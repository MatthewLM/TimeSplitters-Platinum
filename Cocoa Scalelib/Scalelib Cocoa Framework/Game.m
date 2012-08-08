//
//  scalelib.m
//  Scalelib Cocoa Framework
//
//  Created by Matthew Mitchell on 04/07/2010.
//  Copyright 2010 Matthew Mitchell.
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#import "Game.h"
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>

@interface AppDelegate : NSObject{
	ObjCGame *game;
}
@end

@implementation AppDelegate
-(BOOL) applicationShouldTerminateAfterLastWindowClosed:(NSApplication*) sender{
	return YES;
}
-(void) windowDidResize:(NSNotification *) notification{
	[[notification object] center];
}
-(void) windowDidMove:(NSNotification *) notification{
	[[notification object] center];
}
-(NSSize) windowWillResize:(NSWindow *) sender toSize:(NSSize) frameSize{
	NSSize view_size = [game->window contentRectForFrameRect: [game->window frame]].size;
	glViewport(0,0,view_size.width,view_size.height); //Creates the viewport which is mapped to the window
	return frameSize;
}
-(void) windowWillClose:(NSNotification *) notification{
	[game->loop invalidate]; //Stops timer when application closes to prevent segmentation faults.
	[game->section close];
}
-(void) setGame: (ObjCGame *) game_obj{
	game = game_obj;
}
@end

@implementation  OpenGLView
-(void) prepareOpenGL{
	glEnable(GL_BLEND); //Enable alpha blending
	glEnable(GL_TEXTURE_2D); //Enable 2D Textures
	glEnable(GL_POLYGON_SMOOTH); //Enable antialiased polygons
	glEnable(GL_POINT_SMOOTH);
	glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glEnable(GL_MULTISAMPLE_ARB);
	glHint(GL_MULTISAMPLE_FILTER_HINT_NV, GL_NICEST);
	glClearDepth(1.0); // Depth Buffer Setup
	glDepthFunc(GL_EQUAL);
	glDepthMask(GL_TRUE);
	glShadeModel(GL_SMOOTH);
	//Setup 2d View
	[game engage2d];
	//Fade vbo
	glGenBuffers(1,&game->fade_vbo);
	glBindBuffer(GL_ARRAY_BUFFER, game->fade_vbo);
	GLsizeiptr data_size = 8*sizeof(GLdouble);
	GLdouble vertices[] = {0,0,  0,game->game_size[1],  game->game_size[0],0,  game->game_size[0],game->game_size[1]};
	glBufferData(GL_ARRAY_BUFFER, data_size, vertices, GL_STATIC_DRAW);
	//Fog
	glFogi(GL_FOG_MODE,GL_EXP);
	GLfloat colour[] = {1, 1, 1, 0.1}; 
	glFogfv(GL_FOG_COLOR, colour);
	glFogf(GL_FOG_DENSITY, 0.0015);
	glHint(GL_FOG_HINT, GL_FASTEST);
	glFogi(GL_FOG_START, 1);
	glFogi(GL_FOG_END, 1500);
	glFogi(GL_FOG_COORDINATE_SOURCE, GL_FRAGMENT_DEPTH);
}
-(void) setGame: (ObjCGame*) game_obj{
	game = game_obj;
}
-(BOOL) acceptsFirstResponder{
	return YES;
}
-(void) mouseDown:(NSEvent *) event{
	[game pyMouseDown: LEFT_MOUSE_BUTTON];
}
-(void) mouseUp:(NSEvent *) event{
	[game pyMouseUp: LEFT_MOUSE_BUTTON];
}
-(void) keyDown:(NSEvent *) event{
	NSString *characters = [event characters];
	[game pyEventKeyDown: characters];
	@try {
		if ([characters length]){
			[game->keys addObject:[NSNumber numberWithInteger:[[characters lowercaseString] characterAtIndex:0]]];
			game->latest_key = [[characters lowercaseString] characterAtIndex:0];
		}
	} @catch (NSException *exception){
		return;
	}
}
-(void) keyUp:(NSEvent *) event{
	@try {
		NSString *characters = [event characters];
		if ([characters length]){
			[game->keys removeObject:[NSNumber numberWithInteger:[[characters lowercaseString] characterAtIndex:0]]];
		}
	} @catch (NSException *exception){
		return;
	}
}
-(void) mouseMoved:(NSEvent *) event{
	NSPoint new_pos;
	if (game->mouse_tracking){
		int dx,dy;
		CGGetLastMouseDelta(&dx,&dy);
		[game pyMouseMoveX: dx Y: -dy];
	}else{
		new_pos = [self convertPoint: [event locationInWindow] fromView: nil];
		new_pos.y = [game->window contentRectForFrameRect: [game->window frame]].size.height - new_pos.y;
		[game pyMouseMoveX: (int)(new_pos.x - game->mouse_position.x) Y: (int)(game->mouse_position.y - new_pos.y)];
		game->mouse_position = new_pos;
	}
}
-(void) mouseDragged:(NSEvent *) event{
	[self mouseMoved: event];
}
@end

@implementation ObjCGame
-(id) initWithTitle: (NSString*) title_arg Width: (unsigned int) w Height: (unsigned int) h{
	if ( self = [super init] ) {
		title = title_arg;
		game_size[0] = w;
		game_size[1] = h;
		fs = NO; //Fullscreen false to start
		processing_fullscreen = NO;
		fps = -1;
		iconify = NO;
		f_key = NO;
		p_key = NO;
		music_stop = NO;
		event_after_fade = -1;
		fade = 255;
		unfade = YES;
		homedir = [@"~" stringByExpandingTildeInPath];
		fade_screen = NO;
		mouse_position.x = 0;
		mouse_position.y = 0;
		volume = 1;
		mouse_tracking = NO;
		cursor_when_fullscreen = NO;
		exec_dir = [[NSBundle mainBundle] bundlePath];
		//Init arrays
		frames = [NSMutableArray new];
		keys = [NSMutableArray new];
		sections = [NSMutableArray new];
		//Make application
		[NSApplication sharedApplication];
		window = [[NSWindow alloc] initWithContentRect: NSMakeRect(0,0,game_size[0],game_size[1]) styleMask: (NSResizableWindowMask|NSClosableWindowMask|NSTitledWindowMask|NSMiniaturizableWindowMask) backing: NSBackingStoreBuffered defer: NO]; //Make window
		//Setup window
		[window setContentAspectRatio: NSMakeSize (game_size[0],game_size[1])];
		[window setMinSize:NSMakeSize(480, 270)];
		[window zoom:nil];
		[window center];
		[window setMovable:NO];
		[window makeKeyAndOrderFront: nil];
		//Setup OpenGL view 
		NSOpenGLPixelFormatAttribute attrs[] = {NSOpenGLPFADoubleBuffer,NSOpenGLPFAFullScreen,NSOpenGLPFAOffScreen,NSOpenGLPFAAccelerated,NSOpenGLPFAWindow,NSOpenGLPFANoRecovery,NSOpenGLPFAMultisample,NSOpenGLPFASampleBuffers,1,NSOpenGLPFASamples,4,0};
		gfx_view = [[OpenGLView alloc] initWithFrame:NSMakeRect(0, 0, 1280, 720) pixelFormat: [[NSOpenGLPixelFormat alloc] initWithAttributes:attrs]];
		[gfx_view setGame: self];
		AppDelegate *delegate = [[AppDelegate alloc] init];
		[window setContentView: gfx_view];
		[window makeFirstResponder: gfx_view];
		//Setup delegates
		[window setDelegate:delegate];
		[NSApp setDelegate:delegate];
		//Create loop
		loop = [NSTimer scheduledTimerWithTimeInterval: 0.03 target: self selector:@selector(gameLoop:) userInfo:nil repeats:YES];
		//Fire initialisation of sections once the application begins
		[NSTimer scheduledTimerWithTimeInterval: 0 target: self selector:@selector(initSections:) userInfo:nil repeats:NO];
		//Give the delegate the game object
		[delegate setGame: self];
		//setup event array
		events = [[NSMutableArray alloc] init];
		//Set class variable for instance
		clear_colour[0] = 0.0;
		clear_colour[1] = 0.0;
		clear_colour[2] = 0.0;
		clear_colour[3] = 1.0;
	}
	return self;
}
-(BOOL) getFadeScreen{
	return fade_screen;
}
-(BOOL) getUnFade{
	return unfade;
}
-(void) setFadeScreen: (BOOL) boolean{
	fade_screen = boolean;
}
-(unsigned int) getWidth{
	return game_size[0];
}
-(unsigned int) getHeight{
	return game_size[1];
}
-(void) addSection: (id) section_object{
	[sections addObject: section_object];
}
-(void) playMusic: (NSString*) f Volume: (int) vol{
	NSLog(@"Play music method");
	[sound stop];
	sound = [[NSSound alloc] initWithContentsOfFile: f byReference: NO];
	[sound setLoops: YES];
	[sound setVolume: (vol/10.0)];
	[sound play];
}
-(void) setVolume: (int) vol{
	[sound setVolume: (vol/10.0)];
}
-(void) playSound: (NSString*) f Volume: (int) vol{
	NSSound *asound = [[NSSound alloc] initWithContentsOfFile: f byReference: NO];
	[asound setVolume: (vol/10.0)];
	[asound play];
}
-(BOOL) key: (unsigned int) code{
	return [keys containsObject: [NSNumber numberWithInteger:code]];
}
-(BOOL) isFullScreen{
	return fs;
}
-(unsigned short int) getMousePosY{
	return mouse_position.y;
}
-(unsigned short int) getMousePosX{
	return mouse_position.x;
}
-(void) processEnterFullscreen: (NSTimer*) foo{
	fs = YES;
	[self fadeOut];
	[gfx_view enterFullScreenMode:[window screen] withOptions: nil];
	if(!cursor_when_fullscreen){
		[NSCursor hide];
	}
	[self fadeIn];
	processing_fullscreen = NO;
}
-(void) processExitFullscreen: (NSTimer*) foo{
	fs = NO;
	[self fadeOut];
	[gfx_view exitFullScreenModeWithOptions: nil];
	[NSCursor unhide];
	[self fadeIn];
	[window makeFirstResponder: gfx_view];
	processing_fullscreen = NO;
}
-(void) modifyClearColourR: (GLdouble) red G: (GLdouble) green B: (GLdouble) blue A: (GLdouble) alpha {
	clear_colour[0] = red;
	clear_colour[1] = green;
	clear_colour[2] = blue;
	clear_colour[3] = alpha;
}
-(void) gameLoop: (NSTimer*) foo{
	glClearColor(clear_colour[0], clear_colour[1], clear_colour[2], clear_colour[3]);
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
	@try {
		[section loop]; //Loop through section
	} @catch (NSException *exception) {
		NSLog(@"main: Caught %@: %@", [exception name], [exception reason]);
	}
	latest_key = 0;
	if (unfade){
		if (fade < 255){
			[self pyPlayMusic: section];
		}
		if (fade > 0){
			fade -= 200.0/fps;
		}else{
			music_stop = NO;
			unfade = NO;
		}
	}
	if (fade_screen & !unfade){ //Fade out
		if (fade == 0){
			[self playSound: [exec_dir stringByAppendingString: @"/sounds/menu3/fade.ogg"] Volume: [self pyGetVol]];
			music_stop = YES;
		}
		if (fade < 255){
			fade += 200.0/fps;
		}else{
			fade_screen = NO;
			unfade = YES;
		}
	}
	if (!fade_screen){
		if (event_after_fade != -1){
			section = [sections objectAtIndex:event_after_fade];
			[self transfer]; //Transfer to section
			event_after_fade = -1;
		}
	}
	if (fade != 0){
		//Draw fade
		glColor4d(0,0,0,fade/255.0);
		glBindBuffer(GL_ARRAY_BUFFER, fade_vbo);
		glVertexPointer(2, GL_DOUBLE, 0, 0);
		glEnableClientState(GL_VERTEX_ARRAY);
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glDrawArrays(GL_TRIANGLES, 1, 3);
		glDisableClientState(GL_VERTEX_ARRAY);
		glBindBuffer(GL_ARRAY_BUFFER, 0);
	}
	[events removeAllObjects]; //Remove events
	if ([self key: KEY_F]) {
		if (!f_key){
			f_key = YES;
			if (!fs){
				enter_fullscreen = YES;
			}else{
				exit_fullscreen = YES;
			}
		}
	}else{
		f_key = NO;
	}
	if(!processing_fullscreen){
		if (enter_fullscreen){
			processing_fullscreen = YES;
			[NSTimer scheduledTimerWithTimeInterval: 0 target: self selector:@selector(processEnterFullscreen:) userInfo:nil repeats:NO];
		}else if (exit_fullscreen){
			processing_fullscreen = YES;
			[NSTimer scheduledTimerWithTimeInterval: 0 target: self selector:@selector(processExitFullscreen:) userInfo:nil repeats:NO];
		}
	}
	enter_fullscreen = NO;
	exit_fullscreen = NO;
	if (iconify){
		[window performMiniaturize:nil]; //Minimise
		iconify = NO;
	}
	glFlush();
	[frames addObject: [NSDate date]];
	NSTimeInterval time_d = [[frames lastObject] timeIntervalSinceDate: [frames objectAtIndex: ([frames count] - 2)]];
	if (time_d < 0.01667){
		sleep(0.01667 - time_d);
		[frames replaceObjectAtIndex: ([frames count] - 1) withObject: [NSDate date]];
	}
	NSTimeInterval since_first_frame = [[frames lastObject] timeIntervalSinceDate: [frames objectAtIndex: 0]];
	if (since_first_frame > 0){ //Don't do fps for first time especially because it will give a 0 division error
		fps = (short int)([frames count] / since_first_frame);
		if (fps > 60){
			fps = 60;
		}
		int highest_index = -1;
		for(int x = [frames count] - 1;x >= 0 ;x--){
			if ([[frames lastObject] timeIntervalSinceDate: [frames objectAtIndex: x]] > 1){
				highest_index = x + 1;
				break;
			}
		}
		if(highest_index != -1){
			[frames removeObjectsInRange: NSMakeRange(0, highest_index)];
		}
		[window setTitle: [NSString stringWithFormat: @"%@ - %ifps",title, fps]];
	}
}
-(void) fadeIn{
	double fadeInterval = 0.01;
	int step;
	double fader;
	if (curtain_window != nil){
		for (step = 0; step < 100; step++){
			fader = 1.0 - (step * fadeInterval);
			[curtain_window setAlphaValue: fader];
			NSDate *nextDate = [NSDate dateWithTimeIntervalSinceNow: fadeInterval];
			[[NSRunLoop currentRunLoop] runUntilDate: nextDate];
		}
	}
	[curtain_window close];
	curtain_window = nil;
}
-(void) fadeOut{
	double fadeInterval = 0.01;
	int step;
	double fader;
	curtain_window = [[NSWindow alloc] initWithContentRect:[[window screen] frame] styleMask:NSBorderlessWindowMask backing:NSBackingStoreBuffered defer:YES screen: [window screen]];
	[curtain_window setAlphaValue: 0.0];
	[curtain_window setBackgroundColor: [NSColor blackColor]];
	[curtain_window setLevel: NSScreenSaverWindowLevel];
	[curtain_window makeKeyAndOrderFront: nil];
	[curtain_window setFrame:[curtain_window frameRectForContentRect:[[curtain_window screen] frame]] display:YES animate:NO];
	for (step = 0; step < 100; step++){
		fader = step * fadeInterval;
		[curtain_window setAlphaValue: fader];
		NSDate *nextDate = [NSDate dateWithTimeIntervalSinceNow: fadeInterval];
		[[NSRunLoop currentRunLoop] runUntilDate: nextDate];
	}
	[window makeKeyAndOrderFront: nil];
}
-(void) transferSetup: (int) sect{
	event_after_fade = sect;
	fade_screen = YES;
}
-(unsigned short int) getFade{
	return fade;
}
-(void) setSection: (id) section_object{
	section = section_object;
}
-(id) getSection: (NSUInteger) index{
	return [sections objectAtIndex: index];
}
-(id) getCurrentSection{
	return section;
}
-(void) enterFullscreen{
	enter_fullscreen = YES;
}
-(unsigned short int) getFPS{
	return fps;
}
-(unsigned short int) getGameScaledX{
	return [window contentRectForFrameRect: [window frame]].size.width;
}
-(unsigned short int) getGameScaledY{
	return [window contentRectForFrameRect: [window frame]].size.height;
}
-(void) enableMouse{
	[window setAcceptsMouseMovedEvents: YES];
}
-(void) disableMouse{
	[window setAcceptsMouseMovedEvents: NO];
}
-(void) showCursor: (BOOL) show{
	cursor_when_fullscreen = show;
	if(fs){
		if(show){
			[NSCursor unhide];
		}else{
			[NSCursor hide];
		}
	}
}
-(void) trackMouse: (BOOL) track{
	mouse_tracking = track;
	if (track){
		[NSCursor hide];
		NSSize screen = [[NSScreen mainScreen] frame].size;
		CGDisplayMoveCursorToPoint(kCGDirectMainDisplay,(CGPoint){screen.width/2,screen.height/2});
		CGAssociateMouseAndMouseCursorPosition(false);
	}else{
		[NSCursor unhide];
		CGAssociateMouseAndMouseCursorPosition(true);
	}
}
-(int) getLatestKey{
	return latest_key;
}
-(void) engage2d{
	glDisable(GL_LIGHTING);
	glDisable(GL_DEPTH_TEST);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity(); //Load the projection matrix
	gluOrtho2D(0,game_size[0],game_size[1],0); //Set an orthorgraphic view
	glDisable(GL_CULL_FACE);
	glDisable(GL_FOG);
}
-(void) engage3dViewingAngle: (float) viewing_angle Near: (float) near Far: (float) far{
	glEnable(GL_LIGHTING);
	glMatrixMode(GL_PROJECTION); //Select the Ppojection matrix
	glLoadIdentity(); //Load the projection matrix
	gluPerspective(viewing_angle,((float) game_size[0])/game_size[1],near,far); //Setup perspective
	glMatrixMode(GL_MODELVIEW); //Select The Modelview Matrix
	glLoadIdentity();
	glEnable(GL_DEPTH_TEST); //Enables Depth Testing
	GLfloat light_values[] = {1,1,1,1};
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT,light_values);
	glEnable(GL_CULL_FACE);
	glCullFace(GL_FRONT);
	glEnable(GL_FOG);
}
-(void) minimise: (BOOL) state{
	iconify = state;
}
-(void) initSections: (NSTimer*) foo{
	[sections makeObjectsPerformSelector: @selector(initialise)];
}
-(void) start{
	//Run game
	[NSApp run];
}
@end

@implementation PyCocoaThread
-(void) start{
	[NSThread detachNewThreadSelector:@selector(runObjC:) toTarget: self withObject: nil];
}
-(void) runObjC: (id) foo{
	[[NSAutoreleasePool alloc] init];
	[self run];
}
@end

