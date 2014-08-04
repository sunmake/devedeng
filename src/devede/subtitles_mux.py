#!/usr/bin/env python3

# Copyright 2014 (C) Raster Software Vigo (Sergio Costas)
#
# This file is part of DeVeDe-NG
#
# DeVeDe-NG is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# DeVeDe-NG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import devede.configuration_data
import devede.executor

class subtitles_mux(devede.executor.executor):

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def multiplex_subtitles(self,file_path_input, file_path_output, subtitles_path,subt_codepage, subt_lang,
                            subt_upper,font_size, pal, force_subtitles, aspect, duration):

        self.duration = duration
        self.text = _("Adding %(L)s subtitles to %(X)s") % {"X": os.path.basename(file_path_output), "L": subt_lang}

        out_xml = open(file_path_input+".xml","w")
        out_xml.write('<subpictures format="')
        if pal:
            out_xml.write('PAL')
        else:
            out_xml.write('NTSC')
        out_xml.write('">\n')
        out_xml.write('\t<stream>\n')
        out_xml.write('\t\t<textsub filename="')
        out_xml.write(self.expand_xml(subtitles_path))
        out_xml.write('" characterset="')
        out_xml.write(self.expand_xml(subt_codepage))
        out_xml.write('" fontsize="')
        out_xml.write(str(font_size))
        if subt_upper:
            out_xml.write('" bottom-margin="50')
        out_xml.write('" font="arial" horizontal-alignment="center" vertical-alignment="bottom" aspect="')
        out_xml.write(str(aspect))
        out_xml.write('" force="')
        if force_subtitles:
            out_xml.write('yes')
        else:
            out_xml.write('no')
        out_xml.write('" />\n')
        out_xml.write('\t</stream>\n')
        out_xml.write('</subpictures>')
        out_xml.close()
        
        self.command_var=[]
        self.command_var.append("spumux")
        mode = self.config.disc_type
        if mode == "vcd":
            mode = "svcd"
        self.command_var.append("-m")
        self.command_var.append(mode)
        self.command_var.append(file_path_input+".xml")
        self.stdin_file = file_path_input
        self.stdout_file = file_path_output


    def process_stderr(self,data):

        if (data == None) or (len(data) == 0):
            return

        if self.duration == 0:
            return

        if data[0].startswith("STAT: "):
            time_pos = data[0][6:].split(":")
            current_time = 0
            for t in time_pos:
                current_time *= 60
                current_time += float(t)
            t = current_time / self.duration
            self.progress_bar[1].set_fraction(t)
            self.progress_bar[1].set_text("%.1f%%" % (100.0 * t))

        return