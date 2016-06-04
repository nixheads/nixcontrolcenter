#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Johnathan "Shaggytwodope" Jenkins <twodopeshaggy@gmail.com>
#
# Distributed under terms of the GPL2 license.

import os
import sys
import urllib.request
import webbrowser
import subprocess
import fcntl
import tkinter
from configparser import ConfigParser
import gi
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit as webkit
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository.GdkPixbuf import Pixbuf
from os import stat as os_stat
import datetime
import apt


def run_once():
    global fh
    fh = open(os.path.realpath(__file__), 'r')
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        run_once_dialog()


def run_once_dialog():
    window = gtk.Window()
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.WARNING,
                               gtk.ButtonsType.OK, appname + ' - Error')
    dialog.set_default_size(400, 250)
    dialog.set_transient_for(window)
    dialog.format_secondary_text("There is another instance of " + appname +
                                 " already running.")
    response = dialog.run()

    if response == gtk.ResponseType.OK:
        dialog.destroy()
        sys.exit()

    dialog.destroy()


def execute(command, ret=True):
    if ret is True:
        p = os.popen(command)
        return p.readline()
    else:
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        return p.stdout


def functions(view, frame, req, data=None):
    uri = req.get_uri()
    lllink, path = uri.split('://', 1)
    path = path.replace("%20", " ")
    if lllink == "file":
        return False
    elif lllink == "about":
        about = gtk.AboutDialog()
        about.set_program_name(appname)
        about.set_version(appver)
        about.set_copyright('Copyright Linux Lite 2016')
        about.set_wrap_license
        about.set_license(
            '''This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA. ''')
        about.set_authors([
            "Johnathan 'ShaggyTwoDope'" +
            " Jenkins\n<shaggytwodope@linuxliteos.com>\n",
            "Jerry Bezencon\n<valtam@linuxliteos.com>\n",
            "Milos Pavlovic\n<mpsrbija@gmail.com>\n",
            "Brian 'DarthLukan' Tomlinson\n<brian.tomlinson@linux.com>\n",
            "Josh Erickson\n<josh@snoj.us>"
        ])
        about.set_comments("Designed for Linux Lite")
        about.set_website("https://www.linuxliteos.com")
        about.set_logo(Pixbuf.new_from_file(app_icon))
        about.set_transient_for(window)
        about.run()
        about.destroy()
    elif lllink == "admin":
        subprocess.Popen(path, shell=True, executable='/bin/bash')
    elif lllink == "script":
        execute("{0}/scripts/{1}".format(app_dir, path))
    elif lllink == "help":
        webbrowser.open('file:///usr/share/doc/litemanual/index.html')
    elif lllink == "forum":
        webbrowser.open('http://www.linuxliteos.com/forums/')
    elif lllink == "website":
        webbrowser.open('http://www.linuxliteos.com/')
    elif lllink == "facebook":
        webbrowser.open('https://www.facebook.com/linuxliteos')
    elif lllink == "twitter":
        webbrowser.open('http://www.twitter.com/linuxlite/')
    elif lllink == "google":
        webbrowser.open('https://plus.google.com/+linuxliteos/')
    elif lllink == "linkedin":
        webbrowser.open('http://www.linkedin.com/in/jerrybezencon')
    elif lllink == "screenshot":
        os.system("/bin/bash -c 'scrot -u $HOME/nixccshot.png'")
        subprocess.Popen(['/bin/bash', '-c',
                          '/usr/share/nixcc/scripts/screenshot'])
    elif lllink == "report":
        subprocess.Popen(['/bin/bash', '-c', 'gksudo /usr/scripts/systemreport'
                          ])
    elif lllink == "update":
        subprocess.Popen(['/bin/bash', '-c', 'gksudo /usr/scripts/updates-gui'
                          ])
    elif lllink == "refresh":
        reload()

    return True


def reload():
    info = ""
    get_info(info)
    frontend = frontend_fill()
    browser.load_html_string(frontend, "file://{0}/frontend/".format(app_dir))
    return True


def connected(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


def mem_info():
    f = open('/proc/meminfo')
    for line in f:
        if line.startswith('MemTotal:'):
            mem_total = (int(line.split()[1]) * 1024.0)
        elif line.startswith('Active:'):
            mem_active = (int(line.split()[1]) * 1024.0)
        elif line.startswith('Inactive:'):
            mem_inactive = (int(line.split()[1]) * 1024.0)
        elif line.startswith('MemFree:'):
            mem_free = (int(line.split()[1]) * 1024.0)
        elif line.startswith('Cached:'):
            mem_cached = (int(line.split()[1]) * 1024.0)
        elif line.startswith('Buffers:'):
            mem_buffers = (int(line.split()[1]) * 1024.0)
    f.close()

    return (mem_total, mem_active, mem_inactive, mem_free, mem_cached,
            mem_buffers)


def apt_info():
    cache = apt.Cache()
    cache.close()
    cache.open()
    upgrades = 0
    cache.upgrade(dist_upgrade=False)
    changes = cache.get_changes()
    if changes:
        counter = [change.name for change in changes]
        upgrades = (len(counter))
    return upgrades


def get_info(info):
    try:
        if info == "os":
            try:
                osin = open('/etc/llver', 'r').read().split('\\n')[0]
            except:
                infocmd = "lsb_release -d | sed 's/Description:[\t]//g'"
                osin = execute(infocmd).split('\\n')[0]
            return osin
        if info == "desk":
            desk_ses = os.environ.get("XDG_SESSION_DESKTOP")
            if desk_ses is None:
                desk_ses = os.environ.get("XDG_CURRENT_DESKTOP")
            if "XFCE" in desk_ses or desk_ses.startswith("xfce"):
                xfcev = "xfce4-session -V | grep xfce4-session"
                return execute(xfcev).split('(')[1].split(')')[0].split(',')[0]
            elif "ubuntu" in desk_ses:
                return "Unity"
            else:
                return desk_ses
            if desk_ses is None:
                desk_ses = "Desktop Unknown"
                return desk_ses

        if info == "arc":
            return os.uname()[4]
        if info == "host":
            return os.uname()[1]
        if info == "kernel":
            return "{0} {1}".format(os.uname()[0], os.uname()[2])
        if info == "updates":
            pkgcache = '/var/cache/apt/pkgcache.bin'
            aptcount = apt_info()
            if aptcount == 0:
                count = ''
            elif aptcount == 1:
                count = ' (<font style=\"color: red;\">{0}</font> update available)'.format(
                    aptcount)
            else:
                count = ' (<font style=\"color: red;\">{0}</font> updates available)'.format(
                    aptcount)

            if os.path.isfile(pkgcache):
                mtime = os_stat(pkgcache).st_mtime
                modtime = datetime.datetime.fromtimestamp(mtime).strftime(
                    '%Y-%m-%d %H:%M')
                modday = datetime.datetime.fromtimestamp(mtime).strftime(
                    '%Y-%m-%d')
                today = datetime.datetime.today().strftime('%Y-%m-%d')
                if modday == today:
                    updaters = '''<section class="gradient">Last checked on <font style=\"color: green;\">{0}</font>{1} <button style=\"padding-bottom:0px;padding-left:50pxi\" onclick=\"location.href=('update://')\">Run Updates</button></section>'''.format(
                        modtime, count)
                else:
                    updaters = '''<section class="gradient">Last checked on <font style=\"color: red;\">{0}</font>{1} <button style=\"padding-bottom:0px;padding-left:50pxi\" onclick=\"location.href=('update://')\">Run Updates</button></section>'''.format(
                        modtime, count)
            else:
                updaters = '''<section class="gradient">No Update History <button style=\"padding-bottom:0px;padding-left:50pxi\" onclick=\"location.href=('update://')\">Run Updates</button></section>'''

            return updaters

        if info == "processor":
            proc = execute("grep 'model name' /proc/cpuinfo").split(':')[1]
            return proc
        if info == "mem":
            total, active, inactive, free, cached, buffers, = mem_info()
            pie = ((int(total) - int(free)) - (int(buffers) + int(cached)))
            mem_usage = float(pie) * 100 / float(total)
            ramdis = "%14dMB (Used: %8dMB %7.2f%%)" % (
                int(total) / 1048576, pie / 1024 / 1024, mem_usage)

            return ramdis
        if info == "gfx":
            return execute("lspci | grep VGA").split('controller:')[1].split(
                '(rev')[0].split(',')[0]
        if info == "audio":
            audio = execute("lspci | grep 'Audio device:'")
            if len(audio) == 0:
                return execute("lspci | grep audio").split('controller:')[
                    1].split('(rev')[0].split(',')[0]
            else:
                return execute("lspci | grep Audio").split('device:')[1].split(
                    '(rev')[0].split(',')[0]
        if info == "disk":
            p1 = subprocess.Popen(
                ['df', '-Tlh', '--total', '-t', 'ext4', '-t', 'ext3', '-t',
                 'ext2', '-t', 'reiserfs', '-t'
                 'jfs', '-t', 'ntfs', '-t', 'fat32', '-t', 'btrfs', '-t',
                 'fuseblk', '-t', 'xfs'],
                stdout=subprocess.PIPE).communicate()[0].decode("Utf-8")
            total = p1.splitlines()[-1]
            used = total.split()[3].replace(total.split()[3][-1:],
                                            " " + total.split()[3][-1:] + "B")
            size = total.split()[2].replace(total.split()[2][-1:],
                                            " " + total.split()[2][-1:] + "B")
            disk = "{0} (Used: {1})".format(size, used)
            return disk
        if info == "netstatus":
            if connected():
                status = '<font color=green>Active</font>'
            else:
                status = '<font color=red>Not connected</font>'
            return status
        if info == "netip":
            ip = execute("hostname -I").split(' ')
            if len(ip) > 1:
                ip = ip[0]
            elif ip == "":
                ip = 'None'
            else:
                ip = 'None'
            return ip
        if info == "gateway":
            gateway = execute("route -n | grep 'UG[ \t]' | awk '{print $2}'")
            if len(gateway) == 0:
                gateway = 'None'
            return gateway
    except (OSError, TypeError, Exception) as e:
        print(e)
        return " "


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def get_modules(section):
    window = gtk.Window()
    try:
        mod_dir = os.listdir("{0}/modules/{1}/".format(app_dir, section))
        mod_dir.sort()
    except Exception:
        dialog = gtk.MessageDialog(None, 0, gtk.MessageType.WARNING,
                                   gtk.ButtonsType.OK,
                                   'Error Importing Module Data')
        dialog.set_default_size(400, 250)
        dialog.format_secondary_text("No modules could be found." +
                                     " Please reinstall " + appname)
        dialog.set_transient_for(window)
        response = dialog.run()
        if response == gtk.ResponseType.OK:
            dialog.destroy()
            sys.exit()
        dialog.destroy()

    if isinstance(mod_dir, list) and len(mod_dir) < 1:
        return "<p>\"no modules found!\"</p>"
    else:
        parser = ConfigParser()
        admin = ""
        mod_dir.sort()
        for i in mod_dir:
            parser.read("{0}/modules/{1}/{2}".format(app_dir, section, i))
            command = parser.get('module', 'command')

            chk = command.split(' ')[0]
            if chk == "gksudo":
                chk = command.split(' ')[1]
            elif chk == "gksu":
                chk = command.split(' ')[1]
            checking = which(chk)
            if checking is not None:
                ico = parser.get('module', 'ico')
                ico = "{0}/frontend/icons/modules/{1}".format(app_dir, ico)
                name = parser.get('module', 'name')
                desc = parser.get('module', 'desc')
                command = command.replace("'", ''' \\' ''')

                admin += '''<div class="launcher" onclick="location.href='admin://{0}'" >
                <img src="{1}" onerror='this.src = "/usr/share/nixcc/frontend/icons/modules/notfound.png"'/>
                <h3>{2}</h3>
                <span>{3}</span>
                </div>'''.format(command, ico, name, desc)
        return admin


def frontend_fill():
    filee = open("{0}/frontend/default.html".format(app_dir), "r")
    page = filee.read()
    for i in ['os', 'desk', 'arc', 'processor', 'mem', 'gfx', 'audio', 'disk',
              'kernel', 'updates', 'host', 'netstatus', 'netip', 'gateway']:
        page = page.replace("{%s}" % i, str(get_info(i)))
    sections = ['software', 'system', 'desktop', 'hardware', 'networking']
    sections.sort()
    for i in sections:
        page = page.replace("{%s_list}" % i, get_modules(i))
    filee.close()
    return page


def main():
    global browser
    global window
    frontend = frontend_fill()
    window = gtk.Window()
    window.connect('destroy', gtk.main_quit)
    window.set_title(appname)
    window.set_icon(Pixbuf.new_from_file(app_icon))
    rootsize = tkinter.Tk()
    if rootsize.winfo_screenheight() > 700:
        window.set_resizable(False)
        window.set_size_request(880, 660)
    else:
        window.set_resizable(True)
        window.set_size_request(880, 500)
    window.set_position(gtk.WindowPosition.CENTER),
    browser = webkit.WebView()
    swindow = gtk.ScrolledWindow()
    window.add(swindow)
    swindow.add(browser)
    window.show_all()
    browser.connect("navigation-requested", functions)
    browser.load_html_string(frontend, "file://{0}/frontend/".format(app_dir))
    settings = browser.get_settings()
    settings.set_property('enable-default-context-menu', False)
    browser.set_settings(settings)
    gtk.main()


if __name__ == '__main__':
    appname = 'Nix Control Center'
    appver = '1.0'
    app_dir = '/usr/share/nixcc'
    app_icon = "/usr/share/pixmaps/nixcontrolcenter.png"
    fh = 0
    try:
        run_once()
        main()
    except (Exception, AttributeError) as e:
        print("Exiting due to error: {0}".format(e))
        sys.exit(1)
