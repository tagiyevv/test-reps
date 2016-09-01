#!/usr/bin/env python

# Vusal Tagiyev 2014
#
#	A simple program to convert special Azerbaijani charachters to latex
#	fortmat. Do not forget to use "tipa" package for schwa.
#	I couldn't find uppercase schwa. If you ever find it, 
#   please inform me.
#

from gi.repository import Gtk

class SearchDialog(Gtk.Dialog):

	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Search", parent,
			Gtk.DialogFlags.MODAL, buttons=(
			Gtk.STOCK_FIND, Gtk.ResponseType.OK,
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

		box = self.get_content_area()

		label = Gtk.Label("Text to search:")
		box.add(label)

		self.entry = Gtk.Entry()
		box.add(self.entry)	

		self.show_all()

class MainWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Latex Az Char Converter")

		self.set_default_size(350,400)

		hb = Gtk.HeaderBar()
		hb.props.show_close_button = True
		hb.props.title = "Latex Az Char Converter"
		self.set_titlebar(hb)
		
		self.grid = Gtk.Grid()
		self.add(self.grid)
		
		self.create_input()
		self.create_output()

		convert_button = Gtk.Button(label="Convert")
		convert_button.connect("clicked", self.on_convert_clicked)
		self.grid.attach(convert_button,0,2,3,1)
		search_button = Gtk.Button(label="Search")
		search_button.connect("clicked",self.on_search_clicked)
		self.grid.attach(search_button,4,2,3,1)

	def create_input(self):
		input_window = Gtk.ScrolledWindow()
		input_window.set_hexpand(True)
		input_window.set_vexpand(True)
		self.grid.attach(input_window, 0, 1, 3, 1)
		
		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("enter text")
		input_window.add(self.textview)

		self.tag_found = self.textbuffer.create_tag("found", background="blue")

	def create_output(self):
		out_window = Gtk.ScrolledWindow()
		out_window.set_hexpand(True)
		out_window.set_vexpand(True)
		self.grid.attach(out_window,0,3,3,1)
		
		self.text_out = Gtk.TextView()
		self.buffer_out = self.text_out.get_buffer()
		self.buffer_out.set_text(" ")
		out_window.add(self.text_out)

	def on_convert_clicked(self, widget):		
		start = self.textbuffer.get_start_iter()
		end = self.textbuffer.get_end_iter() 
		text_con = self.textbuffer.get_text(start, end, False)
		
		text_con = text_con.replace("\u00FC", "\\\"u").\
							replace("\u011F", "\\u{g}").\
							replace("\u00DC", "\\\"U").\
							replace("\u00FC", "\\\"u").\
							replace("\u00C7", "\\c{C}").\
							replace("\u00E7", "\\c{c}").\
							replace("\u015E", "\\c{S}").\
							replace("\u015F", "\\c{s}").\
							replace("\u00D6", "\\\"O").\
							replace("\u00F6", "\\\"o").\
							replace("\u0131", "{\\i}").\
							replace("\u0130", "\\.{I}").\
							replace("\u0259", "\\textschwa")
							#replace("\u018F", "\\Textschwa")	
	
		#print(text_con)
		
		self.buffer_out.set_text(text_con)

	def on_search_clicked(self, widget):
		dialog = SearchDialog(self)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			cursor_mark = self.textbuffer.get_insert()
			start = self.textbuffer.get_iter_at_mark(cursor_mark)
			if start.get_offset() == self.textbuffer.get_char_count():
				start = self.textbuffer.get_start_iter()

			self.search_and_mark(dialog.entry.get_text(), start)
		
		dialog.destroy()

	def search_and_mark(self, text, start):
		end = self.textbuffer.get_end_iter()
		match = start.forward_search(text, 0 , end)

		if match != None:
			match_start, match_end = match
			self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
			self.search_and_mark(text, match_end)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()			
























