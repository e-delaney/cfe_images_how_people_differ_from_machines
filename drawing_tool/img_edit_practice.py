from tkinter import Tk, Button, Scale, Canvas, Label, StringVar, Entry, \
    Toplevel, messagebox, PhotoImage, ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw
import os
import numpy as np
import pickle
import time


class Images ():
  
  def __init__ (self, path = None):
    
    if path is not None:
      self.npimg = np.load (path);
    else:
      self.npimg = [];

    self.cur = 0;
    
  def get (self):
    this_img = None;
    if self.cur >= 0 and self.cur <= self.npimg.shape[0]:
      this_img = self.npimg[self.cur];

    this_img = this_img[:,:,0].copy ();
    
    # Scaleback from [0,1] to [0, 255]
    this_img = np.round ((this_img - (-0.5)) * 255);
    this_img = this_img.astype (np.uint8);
    
    return (this_img);
  
  def next (self):
    self.cur = self.cur + 1;
    if self.cur >= self.npimg.shape[0]:
      self.cur = self.npimg.shape[0] - 1;
  
  def prev (self):
    self.cur = self.cur - 1;
    if self.cur < 0:
      self.cur = 0;
  
  def get_idx (self):
    return self.cur;
  
  def len (self):
    return (len (self.npimg));
  
  def set (self, arr):
    
    arr = arr.astype ('float32');
    arr /= 255.0;
    arr = arr - 0.5;
    
    self.npimg[self.cur] = arr;
  
  
  def save (self, file_name):
    np.save (file_name, self.npimg);

    
class CFGen ():
  DEFAULT_PEN_SIZE = 15.0;  
  DEFAULT_COLOUR = "white";
  INVERSE_COLOUR = "black";
  CANVAS_W = 600;
  CANVAS_H = 600;
  UNDO_STEPS = 10;
  LARGE_FONT = ("Verdana", 12);
  NORM_FONT  = ("Verdana", 10);
  SMALL_FONT = ("Verdana", 8);

  # TODO: file existance check, so that things go smoothly.
  def __init__ (self, img_path, save_file_path = None, class_misclass_pair_file = None, img_msg_formatstr = None, stroke_file_path = None, load_stroke_info = False, help_file_path = r"C:\Users\eoind\Desktop\interface_prototype-main_V3\interface_prototype-main\g2_formatstr.txt", show_help_default = False, height = 600, width = 600):
    
    self.save_file_path = save_file_path;
    if self.save_file_path is None:
      self.save_file_path = img_path.split (".")[0] + "_edited." + img_path.split (".")[1];

    self.stroke_file_path = stroke_file_path;
    #print (self.stroke_file_path);
    if self.stroke_file_path is None:
      self.stroke_file_path = self.save_file_path.split (".")[0] + "_stroke_" + self.save_file_path.split (".")[1] + ".pkl";

    self.class_misclass_pair_file = None;
    if class_misclass_pair_file is not None:
      self.class_misclass_pair_file = class_misclass_pair_file;

    # TODO: See if the files we are working with exists or not.


    # TODO: Validate window size
    #width = 100 if width < 100 else print ("df") ;
    #height = 100 if height < 100 else print ("df");

    self.CANVAS_W = width;
    self.CANVAS_H = height;

    self.cur_dstack = [];

    self.win = Tk ();
    # Place at the centre of the screen
    self.win.eval("tk::PlaceWindow . center");
    self.win.title ("CFGen");
    self.win.resizable (False, False);
    self.win.protocol ("WM_DELETE_WINDOW", self.quit_window);



    """self.draw_button = Button (self.win, text = "Draw", command = self.draw);
    self.draw_button.grid (row = 0, column = 0, sticky = "ew", padx = 5, pady = 2);
    
    self.erase_button = Button (self.win, text = "Erase", command = self.erase);
    self.erase_button.grid (row = 1, column = 0, sticky = "ew", padx = 5, pady = 2);

    self.size_scale = Scale (self.win, label = "Brush Size", from_ = 2, to = 6, orient = "horizontal");
    self.size_scale.grid (row = 0, column = 1, rowspan = 2, sticky = "ew", padx = 5, pady = 2);

    self.next_image_button = Button (self.win, text = "Next", command = self.next_image);
    self.next_image_button.grid (row = 0, column = 2, sticky = "ew", padx = 5, pady = 2);
      
    self.prev_image_button = Button (self.win, text = "Prev", command = self.prev_image);
    self.prev_image_button.grid (row = 1, column = 2, sticky = "ew", padx = 5, pady = 2);
    
    self.load_original = Button (self.win, text = "Reload Original", command = self.reload_original);
    self.load_original.grid (row = 1, column = 4, sticky = "ew", padx = 5, pady = 2);
      
    self.undo_button = Button (self.win, text = "Undo", command = self.undo);
    self.undo_button.grid (row = 0, column = 3, sticky = "ew", padx = 5, pady = 2);
    
    self.help_button = Button (self.win, text = "Instructions", command = self.instructions);
    self.help_button.grid (row = 0, column = 4, sticky = "ew", padx = 5, pady = 2);

    # Make package once all is done
    self.submit_button = Button (self.win, text = "Save", command = self.save_changes);
    self.submit_button.grid (row = 1, column = 3, sticky = "ew", padx = 5, pady = 2);

    self.message = StringVar (value = "");
    self.message_area = Label (self.win, textvariable = self.message, font = self.LARGE_FONT, wraplength = self.CANVAS_W, justify = "left");
    self.message_area.grid (row = 2, column = 0, rowspan = 4, columnspan = 6, padx = 5, pady = 15);
    
    self.c = Canvas (self.win, bg = "white", width = self.CANVAS_W, height = self.CANVAS_H, cursor = "dot");
    self.c.grid (row = 6, columnspan = 5);
    
    self.var_status = StringVar (value = "Selected: Draw");
    self.label_status = Label (self.win, textvariable = self.var_status);
    self.label_status.grid (row = 7, column = 4, rowspan = 3);"""
    
    
    self.draw_button = Button (self.win, text = "Draw", command = self.draw);
    self.draw_button.grid (row = 0, column = 0, columnspan=2,rowspan=2, sticky = "ew", padx = 5, pady = 2);
    
    self.erase_button = Button (self.win, text = "Erase", command = self.erase);
    self.erase_button.grid (row = 0, column = 3, columnspan=2,rowspan=2, sticky = "ew", padx = 5, pady = 2);

    self.size_scale = Scale (self.win, label = "    Stroke Size", from_ = 2, to = 5, orient = "horizontal");
    """self.size_scale.grid (row = 0, column = 2, rowspan = 2, sticky = "ew", padx = 5, pady = 2);"""

    """self.next_image_button = Button (self.win, text = "Next", command = self.next_image);
    self.next_image_button.grid (row = 0, column = 2, sticky = "ew", padx = 5, pady = 2);"""
      
    """self.prev_image_button = Button (self.win, text = "Prev", command = self.prev_image);
    self.prev_image_button.grid (row = 1, column = 2, sticky = "ew", padx = 5, pady = 2);"""
    
    self.load_original = Button (self.win, text = "Reset", command = self.reload_original);
    self.load_original.grid (row = 8, column = 4,columnspan=3, sticky = "ew", padx = 5, pady = 2);
      
    """self.undo_button = Button (self.win, text = "Undo", command = self.undo);
    self.undo_button.grid (row = 0, column = 3, sticky = "ew", padx = 5, pady = 2);"""
    
    """self.help_button = Button (self.win, text = "Instructions", command = self.instructions);
    self.help_button.grid (row = 0, column = 4, sticky = "ew", padx = 5, pady = 2);"""

    # Make package once all is done
    self.submit_button = Button (self.win, text = "Save", command = self.save_changes);
    """self.submit_button.grid (row = 1, column = 3,columnspan=3, sticky = "ew", padx = 5, pady = 2);"""

    self.message = StringVar (value = "");
    self.message_area = Label (self.win, textvariable = self.message, font = self.LARGE_FONT, wraplength = self.CANVAS_W, justify = "left");
    self.message_area.grid (row = 2, column = 0, rowspan = 4, columnspan = 6, padx = 5, pady = 15);
    
    self.c = Canvas (self.win, bg = "white", width = self.CANVAS_W, height = self.CANVAS_H, cursor = "dot");
    self.c.grid (row = 6, columnspan = 5);
    
    self.var_status = StringVar (value = "Selected: Draw");
    self.label_status = Label (self.win, textvariable = self.var_status);
    """self.label_status.grid (row = 7, column = 4, rowspan = 3);"""
    
    
    self.next_image_button = Button (self.win, text = u"Next Task \u21E8", command = self.next_image);
    self.next_image_button.grid (row = 8, column = 2, columnspan=2, sticky = "ew", padx = 5, pady = 2);
      
    self.prev_image_button = Button (self.win, text = u"\u21E6", command = self.prev_image);
    self.prev_image_button.grid (row = 8, column = 0,columnspan =2, sticky = "ew", padx = 5, pady = 2);
    
    
    
    
    # Read the images
    self.imgs      = Images (img_path);
    self.imgs_edit = Images (img_path); # Continually keep saving the changes here
    self.dstack = [];

    self.help_file_path = help_file_path;

    fd = open (self.help_file_path);
    self.help_message = fd.read ();
    fd.close ();

    # If `img_msg_formatstr' is a file then read the format string from file
    # Else just keep using the passed string as the format string
    # If `img_msg_formatstr' is None then use the default string
    self.img_msg_formatstr = img_msg_formatstr;

    if self.img_msg_formatstr is None or os.path.isfile (self.img_msg_formatstr) == False:
      print ("Setting default image format string");
      self.img_msg_formatstr = "The image is labelled as %predicted, what would you do to change it to %true";

    if os.path.isfile (self.img_msg_formatstr):
      print ("Reading format string from file");
      fd = open (self.img_msg_formatstr);
      self.img_msg_formatstr = fd.read ();
      fd.close ();

    # NOTE: Check if the format string actuallt is valid. Can skip for now.


    # NOTE: Assuming `img_labels' format as [predicted, true] for each entry
    self.img_labels = np.load (self.class_misclass_pair_file);

    if len (self.img_labels) != self.imgs.len ():
      messagebox.warning (f"WARNING: class_misclass_pair_file \"{self.class_misclass_pair_file}\" is not the same length of the number of images");
      #print (f"WARNING: class_misclass_pair_file \"{self.class_misclass_pair_file}\" is not the same length of the number of images");
      # TODO: Decide if to throw exception or not.

    if load_stroke_info == True:
      self.load_stroke_info ();

    self.draw_toggle = False;

    for i in range (self.imgs.len()):
      self.dstack.append ([]);
    #print (self.dstack);

    self.active_button = None;

    self.setup ();
    self.show_img ();
    self.cur_dstack = self.dstack[self.imgs.get_idx ()];
    self.redraw_stack ();
    self.draw ();

    #self.instructions ();
    self.win.mainloop ();

    
  def draw (self):
    self.enable_button (self.draw_button);

  def erase (self):
    self.enable_button (self.erase_button, eraser_mode = True);
  
  def next_image (self):
    #print (self.dstack); 

    # Load the operator stack of this image, display image, redraw
    self.dstack[self.imgs.get_idx ()] = self.cur_dstack;
    
    self.imgs_edit.set (self.merge_raster ());
    self.imgs_edit.next ();
    
    self.imgs.next ();
    self.cur_dstack = self.dstack[self.imgs.get_idx ()];
    self.show_img ();
    self.redraw_stack ();
    
    self.draw(); #draw by default
 
    
  def prev_image (self):
    #print (self.dstack); 
    

    # Load the operator stack of this image, display image, redraw
    self.dstack[self.imgs.get_idx ()] = self.cur_dstack;

    self.imgs_edit.set (self.merge_raster ());
    self.imgs_edit.prev ();
    
    self.imgs.prev ();  
    self.cur_dstack = self.dstack[self.imgs.get_idx ()];
    self.show_img ();
    self.redraw_stack ();
    
    self.draw(); #draw by default

  
  def reload_original (self):
    # Empty stack, forget everything, reload original, redraw
    self.cur_dstack = [];
    self.dstack[self.imgs.get_idx ()] = self.cur_dstack;

    self.imgs_edit.set (self.merge_raster ());
    #self.imgs_edit.prev ();
    
    self.show_img ();
    self.redraw_stack ();

    #self.enable_button (self.load_original);
    
  def show_img (self):
    self.this_img = self.to_tkinter (self.imgs.get ());
    self.c.create_image (0, 0, image = self.this_img, anchor = "nw");
    self.show_img_msg ();



  def undo (self, event = None):

    for i in range (self.UNDO_STEPS):
      if len (self.cur_dstack) > 0:
        canvas_oper = self.cur_dstack.pop (); # remove from operation stack
        if canvas_oper is not None:
          self.c.delete (canvas_oper[4]); # remove from canvas
  
  #def undo (self):
    #print (self.cur_dstack);
    #print ("######");
    ##for i in range (self.UNDO_STEPS):
      ##if len (self.cur_dstack) > 0:
        ##canvas_oper = self.cur_dstack.pop (); # remove from operation stack
        ##if canvas_oper is not None:
          ##self.c.delete (canvas_oper[4]); # remove from canvas

    ##for i in range (self.UNDO_STEPS):
      ##if len (self.cur_dstack) > 0:
        ##if canvas_oper is not None:
          ##self.c.delete (canvas_oper[4]); # remove from canvas
    #self.cur_dstack.insert (len (self.cur_dstack) - self.UNDO_STEPS, None);
    #i = 0;
    #while i in range (len (self.cur_dstack)):
      #if self.cur_dstack[i] is None:
        #i += 1;
        #break;


    #j = len (self.cur_dstack);
    #while i < j:
      #print (i, j);
      #self.c.delete (self.cur_dstack[i][4]);
      #i += 1;
  
  # TODO: NO REDO YET, we will need stack pointer for that, or additional stack
  def redo (self):
    pass;
    #self.enable_button (self.redo_button);

  def save_changes (self):
    self.imgs_edit.save (self.save_file_path);
    self.save_stroke_info ();

  def quit_window (self):
    ync_val = messagebox.askyesnocancel (title = "Quit", message = "Do you want to save?", default = messagebox.YES);
    if ync_val == True:
      self.save_changes ();
      self.win.destroy ();
      print ("Saved and quit successfully");
    elif ync_val == False:
      self.win.destroy ();
      print ("NOT Saved and quit successfully");

  def instructions (self):
    print (self.help_message);

    popup = Tk ();
    popup.title ("Instructions");
    label = ttk.Label (popup, text = self.help_message, font = self.LARGE_FONT);
    label.pack (side = "top", fill = "x", pady = 2);
    B1 = ttk.Button (popup, text = "Ok", command = popup.destroy);
    B1.pack ();
    popup.eval ("tk::PlaceWindow . center");
    popup.mainloop ();

  # Display the instruction for this image
  def show_img_msg (self):
    if self.img_labels is not None:
      this_pair = self.img_labels[self.imgs.get_idx ()];
      this_format_str = self.img_msg_formatstr;
      this_format_str = this_format_str.replace ("%true", str (this_pair[1]));
      this_format_str = this_format_str.replace ("%predicted", str (this_pair[0]));
      self.message.set (this_format_str);



  def save_stroke_info (self):
    with open (self.stroke_file_path, "wb") as fp:
        pickle.dump (self.dstack, fp);

  def load_stroke_info (self):
    with open (self.stroke_file_path, "rb") as fp:
        self.dstack = pickle.load (fp);

  def submit (self):
    self.imgs_edit.save (self.save_file_path);
  
  
  ## Keeping this method here.
  #def canvas_to_numpy (self):
    #canvas.postscript (file = "tmp_canvas.eps", colourmode = "colour", width = CANVAS_WIDTH, height = CANVAS_HEIGHT, pagewidth = CANVAS_WIDTH - 1, pageheight = CANVAS_HEIGHT - 1);
    #data = ski_io.imread("tmp_canvas.eps");
    #ski_io.imsave("canvas_image.png", data);
    #pass;
    
  
  def setup (self):
    self.colour         = self.DEFAULT_COLOUR;
    self.erase_colour   = self.INVERSE_COLOUR;
    self.eraser_on      = False;

    #self.active_button  = self.draw_button;
    self.draw ();
    self.old_x, self.old_y = None, None;
    self.size_multiplier   = self.DEFAULT_PEN_SIZE;
    
    self.c.bind ("<B1-Motion>", self.paint);
#    self.c.bind ("<B3-Motion>", self.paint_b3);

    self.c.bind ("<ButtonRelease-1>", self.reset);
    self.c.bind ("<ButtonRelease-3>", self.reset);

    self.c.bind ("<Button-1>", self.point);
#    self.c.bind ("<Button-3>", self.point_b3);

    self.win.bind ("<Control-z>", self.undo);

    self.win.bind ("<Escape>", self.line_reset);

    self.line_start = (None, None);
  
    
  def enable_button (self, button_name, eraser_mode = False):
    if self.active_button:
      self.active_button.config (relief = "raised");
    button_name.config (relief = "sunken");
    self.active_button = button_name;
    self.eraser_on = eraser_mode;
    self.set_status ();
    
  def line (self, x, y):
    line_width = self.size_scale.get() * self.size_multiplier;
    line_width = int (np.round (line_width)); # Convert to int
    paint_colour = self.erase_colour if self.eraser_on else self.colour
    self.c.create_line(self.line_start[0], self.line_start[1], x, y,
                        width = line_width, fill = paint_colour,
                        capstyle = "round", smooth = True, splinesteps = 36)
    
  
  def point_b3 (self, event):
    self.erase ();
    self.point (event);
    self.draw ();

  def point (self, event):
    #print  ("POINT");
    #if event.num == 3 and self.eraser_on == False:
      #self.erase ();
      #self.draw_toggle = True;

    self.set_status(event.x, event.y);
    line_width = self.size_scale.get() * self.size_multiplier;
    line_width = int (np.round (line_width)); # Convert to int
    paint_colour = self.erase_colour if self.eraser_on else self.colour;
    btn = self.active_button["text"];
    oper = self.c.create_oval (event.x, event.y, event.x, event.y, fill = paint_colour, outline = paint_colour, width = line_width);
    self.cur_dstack.append ([event.x, event.y, self.eraser_on, line_width, oper, "point"]);

    self.old_x = event.x;
    self.old_y = event.y;

    #if event.num == 3 and self.eraser_on == True:
      #self.draw ();
      #self.draw_toggle = False;
    #print (self.dstack);

  def paint_b3 (self, event):
    self.erase ();
    self.paint (event);
    self.draw ();
            
  def paint (self, event):
    #print  ("PAINT");
    #print (event.num);
    #print (event.state);

    self.set_status (event.x, event.y);
    line_width = self.size_scale.get() * self.size_multiplier;
    line_width = int (np.round (line_width)); # Convert to int
    paint_colour = self.erase_colour if self.eraser_on else self.colour;
    if self.old_x and self.old_y:
        oper = self.c.create_line (self.old_x, self.old_y, event.x, event.y,
                            width = line_width, fill = paint_colour,
                            capstyle = "round", smooth = True, splinesteps = 36);
        self.cur_dstack.append ([event.x, event.y, self.eraser_on, line_width, oper, "paint"]);

    self.old_x = event.x;
    self.old_y = event.y;

  def redraw_stack (self):
    old_x, old_y = None, None;
    if self.cur_dstack is not None:
      for this_opt_idx in range (len (self.cur_dstack)):
        #time.sleep (0.001);
        this_opt = self.cur_dstack[this_opt_idx];
        if this_opt is None:
          break;
        # Draw if the operation stack is not empty
        if this_opt is not None:
          paint_colour = self.erase_colour if this_opt[2] else self.colour
          if this_opt[5] == "point":
            this_opt[4] = self.c.create_oval (this_opt[0], this_opt[1], this_opt[0], this_opt[1], fill = paint_colour, outline = paint_colour, width = this_opt[3]);
            #old_x, old_y = None, None;
          elif this_opt[5] == "paint":
            if old_x and old_y:
              this_opt[4] = self.c.create_line (old_x, old_y, this_opt[0], this_opt[1],
                                  width = this_opt[3], fill = paint_colour,
                                  capstyle = "round", smooth = True, splinesteps = 36);
          old_x = this_opt[0];
          old_y = this_opt[1];
          self.cur_dstack[this_opt_idx] = this_opt;
          #self.win.update_idletasks (); # Update canvas when using the time.sleep ();


  # TODO: A version of merge raster which saves file in steps and write to pipe/regular file to be read by other programs.
  def merge_raster (self, w = None, h = None):
    width = w;
    height = h;
    if width == None or height == None:
      width = self.CANVAS_W;
      height = self.CANVAS_H;
    
    ras_img = Image.fromarray (self.imgs.get (), mode = "L");
    width_orig = ras_img.width;
    height_orig = ras_img.height;
    
    ras_img = ras_img.resize ((width, height), Image.ANTIALIAS);
    ras_draw = ImageDraw.Draw (ras_img);
    
    old_x, old_y = None, None;
    if self.cur_dstack is not None:
      for this_opt in self.cur_dstack:
        # Draw if the operation stack is not empty
        if this_opt is not None:
          paint_colour = self.erase_colour if this_opt[2] else self.colour;
          if this_opt[5] == "point":  
            ras_draw.ellipse ((this_opt[0], this_opt[1], this_opt[0], this_opt[1]), fill = paint_colour, outline = paint_colour, width = this_opt[3]);
            #old_x, old_y = None, None;
          elif this_opt[5] == "paint":
            if old_x and old_y:
              ras_draw.line ((old_x, old_y, this_opt[0], this_opt[1]), fill = paint_colour, width = this_opt[3], joint = "curve");

          old_x = this_opt[0];
          old_y = this_opt[1];
          
    ras_img = ras_img.resize ((width_orig, height_orig));
    ras_img = ras_img.convert ('L');
    ras_img = np.array(ras_img);
    ras_img = ras_img.reshape (-1, width_orig, height_orig, 1);
    
    return (ras_img);


  # TODO: Save stroke information. Have a replay button or execute button to redo the stuff.
  def get_stroke_info (self):
    return (self.dstack);
  
  
  def line_reset(self, event):
      self.line_start = (None, None)

  def reset(self, event):
    self.old_x, self.old_y = None, None

  def set_status (self, x = None, y = None):
    if self.active_button:
        btn = self.active_button["text"];
        self.var_status.set (f"Selected: {btn}");

  def to_tkinter (self, this_img, w = None, h = None):                          
    width = w;
    height = h;
    if width == None or height == None:
      width = self.CANVAS_W;
      height = self.CANVAS_H;
    
    img = Image.fromarray (this_img, mode = "L");
    img = img.resize ((width, height), Image.ANTIALIAS);
    img = ImageTk.PhotoImage (image = img);
    
    return (img);
  
  
  def from_tkinter (self, this_img, w = None, h = None):
    pass;



# TODO: Documentation
# TODO: Save in different directories, ask before overwriting. Give printed message where they were stored,
# TODO: Better button generalisation, put all in hashmap, automated button generation
# TODO: We keep on saving a copy of rastarised image as we continue, this may not be efficient in case of large datasets. Although this feature is not needed in our application.
if __name__ == "__main__":
  #CFGen (img_path = "ICLR_22/misclassified_image_set.npy", save_file_path = "cfe_demo.npy", stroke_file_path = None);
  # This will load the npy file in `img_path', edited npy will be in `save_file_path', The stroke details will be in `stroke_file_path', If `load_stroke_info' is True, and the `stroke_file_path' exists, then and older stroke file will also be loaded.
  # TODO: load_stroke_info should as yesno before overwriting. Any result file should prompt before overwriting and if possible ask for new filename.
  CFGen (img_path = r"C:/Users/eoind/Desktop/interface_prototype-main_V3/interface_prototype-main/ICLR_22/misclassified_image_practice_set.npy", save_file_path = "cfe_practice.npy", img_msg_formatstr = r"C:\Users\eoind\Desktop\interface_prototype-main_V3\interface_prototype-main\g2_formatstr.txt", class_misclass_pair_file = r"C:/Users/eoind/Desktop/interface_prototype-main_V3/interface_prototype-main/ICLR_22/misclassification_pairs_practice_mnist.npy", stroke_file_path = "cfe_practice_npy.pkl", load_stroke_info = False, show_help_default = False);
  #CFGen ("ICLR_22/misclassified_image_set.npy");
  #CFGen ("cfe_demo.npy");
