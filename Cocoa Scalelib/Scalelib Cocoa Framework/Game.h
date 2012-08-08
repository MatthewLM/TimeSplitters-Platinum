//
//  scalelib.h
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

#import <Cocoa/Cocoa.h>

//Constants
#define KEY_F 102
#define LEFT_MOUSE_BUTTON 0

@interface ObjCGame : NSObject {
	@public
	BOOL fs;
	unsigned short int game_scaled[2];
	unsigned short int game_size[2];
	NSString *title;
	unsigned short int fps;
	BOOL iconify;
	BOOL f_key;
	BOOL p_key;
	BOOL music_stop;
	BOOL unfade;
	float fade;
	int event_after_fade;
	NSString *homedir;
	BOOL fade_screen;
	NSMutableArray *keys;
	NSMutableArray *sections;
	id section;
	NSMutableArray *frames;
	int volume;
	NSWindow *window;
	NSWindow *curtain_window;
	id gfx_view;
	CGDisplayFadeReservationToken token;
	BOOL enter_fullscreen;
	BOOL exit_fullscreen;
	NSPoint mouse_position;
	NSTimer *loop;
	NSSound *sound;
	BOOL processing_fullscreen;
	BOOL mouse_tracking;
	BOOL cursor_when_fullscreen;
	NSString *exec_dir;
	GLuint fade_vbo;
	int  latest_key;
	GLdouble clear_colour[4];
	NSMutableArray * events;
	NSMutableArray * options;
	NSMutableArray * controls;
	BOOL scale_to_screen;
}
-(id) initWithTitle: (NSString*) title_arg Width: (unsigned int) w Height: (unsigned int) h;
-(void) addSection: (id) section_object;
-(void) playMusic: (NSString*) f Volume: (int) vol;
-(void) gameLoop;
-(void) start;
-(void) fadeIn;
-(void) fadeOut;
-(void) transferSetup: (int) sect;
-(unsigned short int) getFade;
-(void) setSection: (id) section_object;
-(id) getSection: (NSUInteger) index;
-(void) enterFullscreen;
-(unsigned int) getWidth;
-(unsigned int) getHeight;
-(BOOL) getFadeScreen;
-(void) setFadeScreen: (BOOL) boolean;
-(BOOL) getUnFade;
-(id) getCurrentSection;
-(unsigned short int) getFPS;
-(BOOL) isFullScreen;
-(unsigned short int) getMousePosY;
-(unsigned short int) getMousePosX;
- (unsigned short int) getGameScaledX;
- (unsigned short int) getGameScaledY;
-(void) playAgain:(NSNotification*) note;
-(void) playSound: (NSString*) f Volume: (int) vol;
-(void) setVolume: (int) vol;
-(void) processEnterFullscreen: (NSTimer*) foo;
-(void) processExitFullscreen: (NSTimer*) foo;
-(void) initSections: (NSTimer*) foo;
-(void) trackMouse: (BOOL) track;
-(void) showCursor: (BOOL) show;
-(void) minimise: (BOOL) state;
-(int) getLatestKey;
-(void) engage3dViewingAngle: (float) viewing_angle Near: (float) near Far: (float) far;
-(void) engage2d;
-(void) modifyClearColourR: (GLdouble) red G: (GLdouble) green B: (GLdouble) blue A: (GLdouble) alpha;
@end

@interface OpenGLView : NSOpenGLView{
	ObjCGame *game;
}
- (void) prepareOpenGL;
- (void) setGame: (ObjCGame *) game_obj;
- (BOOL) acceptsFirstResponder;
- (void) mouseDown:(NSEvent *) event;
- (void) mouseUp:(NSEvent *) event;
- (void) keyDown:(NSEvent *) event;
- (void) keyUp:(NSEvent *) event;
@end

@interface PyCocoaThread : NSObject{
}
-(void) start;
-(void) runObjC: (id) foo;
@end