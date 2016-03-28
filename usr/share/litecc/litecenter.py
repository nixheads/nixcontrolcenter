import os
import re
import sys
import urllib.request
import webbrowser
import subprocess
import fcntl
import tkinter
from configparser import ConfigParser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository.GdkPixbuf import Pixbuf
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit as webkit

app_dir = '/usr/share/litecc'

"""lock the file so no two instances can run"""
fh = 0


def run_once():
    global fh
    fh = open(os.path.realpath(__file__), 'r')
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        sys.exit(0)


def execute(command, ret=True):
    """function to exec everything, subprocess used to fork"""

    if ret is True:
        p = os.popen(command)
        return p.readline()
    else:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        return p.stdout


def functions(view, frame, req, data=None):
    """base functions"""
    uri = req.get_uri()
    lllink, path = uri.split('://', 1)
    path = path.replace("%20", " ")
    print(lllink)
    print(uri)
    if lllink == "file":
        return False
    elif lllink == "about":
        '''about dialog, need to add LDC members whom helped'''
        about = gtk.AboutDialog()
        about.set_program_name("Linux Lite Control Center")
        about.set_version("1.0-0250")
        about.set_license('''This program is free software; you can redistribute it and/or modify it
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
        about.set_authors(
            [
                "Johnathan 'ShaggyTwoDope' Jenkins\n<shaggytwodope@linuxliteos.com>\n",
                "Jerry Bezencon\n<valtam@linuxliteos.com>\n",
                "Milos Pavlovic\n<mpsrbija@gmail.com>\n",
                "Brian 'DarthLukan' Tomlinson\n<brian.tomlinson@linux.com>\n",
                "Josh Erickson\n<josh@snoj.us>"
            ]
        )
        about.set_comments("Designed for Linux Lite")
        about.set_website("http://www.linuxliteos.com")
        about.set_logo(Pixbuf.new_from_file("{0}/litecc.png".format(app_dir)))
        about.run()
        about.destroy()
    elif lllink == "admin":
        subprocess.Popen(path, shell=True, executable='/bin/bash')
    # uses executep to pipe process fork
    elif lllink == "script":
        execute("{0}/scripts/{1}".format(app_dir, path))
    # need to fix urls
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
        os.system("/bin/bash -c 'scrot -u $HOME/liteccshot.png'")
        subprocess.Popen(['/bin/bash', '-c',
                          '/usr/share/litecc/scripts/screenshot'])
    elif lllink == "report":
        subprocess.Popen(['/bin/bash', '-c',
                          'gksudo /usr/scripts/systemreport'])
    elif lllink == "update":
        subprocess.Popen(['/bin/bash', '-c',
                          'gksudo /usr/scripts/updates-gui'])
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


def get_info(info):
    """here we gather some over all basic info"""
    try:
        if info == "os":
            try:
                osin = open('/etc/llver', 'r').read().split('\\n')[0]
            except:
                osin = execute("lsb_release -d | sed 's/Description:[\t]//g'").split('\\n')[0]
            return osin
        if info == "desk":
            desk_ses = os.environ.get("XDG_CURRENT_DESKTOP")
            if desk_ses in ["gnome", "unity", "cinnamon", "mate", "xfce4",
                            "lxde", "fluxbox", "blackbox", "openbox", "icewm",
                            "jwm", "afterstep", "trinity", "kde"]:
                return desk_ses
            # This is hacky but oh well
            elif "XFCE" in desk_ses or desk_ses.startswith("xfce"):
                return execute("xfce4-session -V | grep xfce4-session").split('(')[1].split(')')[0].split(',')[0]
        if info == "arc":
            return os.uname()[4]
        if info == "host":
            return os.uname()[1]
        if info == "kernel":
            return "{0} {1}".format(os.uname()[0], os.uname()[2])
        if info == "updates":
            return execute("/usr/share/litecc/scripts/updates")
        if info == "processor":
            proc = execute("grep 'model name' /proc/cpuinfo").split(':')[1]
            return proc
        if info == "mem":
            raminfo = subprocess.Popen(
                ['free', '-m'], stdout=subprocess.PIPE).communicate()[0].decode('Utf-8').split('\n')
            ram = ''.join(filter(re.compile('M').search, raminfo)).split()
            used = int(ram[2]) - int(ram[5]) - int(ram[6])
            usedpercent = "%.1f" % ((float(used) / float(ram[1])) * 100)
            ramdis = "{0} MB  (Used: {1} MB {2}%)".format(ram[1], used,
                                                          usedpercent)
            return ramdis
        if info == "gfx":
            return execute("lspci | grep VGA").split('controller:')[1].split('(rev')[0].split(',')[0]
        if info == "audio":
            audio = execute("lspci | grep 'Audio device:'")
            if len(audio) == 0:
                return execute("lspci | grep audio").split('controller:')[1].split('(rev')[0].split(',')[0]
            else:
                return execute("lspci | grep Audio").split('device:')[1].split('(rev')[0].split(',')[0]
        if info == "disk":
            p1 = subprocess.Popen(['df', '-Tlh', '--total', '-t', 'ext4', '-t',
                                   'ext3', '-t', 'ext2', '-t', 'reiserfs', '-t'
                                   'jfs', '-t', 'ntfs', '-t', 'fat32', '-t',
                                   'btrfs', '-t', 'fuseblk', '-t', 'xfs'],
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
    """we try and load errrors"""
    try:
        mod_dir = os.listdir("{0}/modules/{1}/".format(app_dir, section))
        mod_dir.sort()
    except Exception as details:
        os.system(
            "zenity --error --text 'Error : {0}' --title 'Module Loading Error'".format(details))
        return exit()

    if isinstance(mod_dir, list) and len(mod_dir) < 1:
        return "<p>\"no modules found!\"</p>"
    else:
        parser = ConfigParser()
        admin = ""
        mod_dir.sort()
        for i in mod_dir:
            parser.read("{0}/modules/{1}/{2}".format(app_dir, section, i))

            # get the command from module
            command = parser.get('module', 'command')

            chk = command.split(' ')[0]
            if chk == "gksudo":
                chk = command.split(' ')[1]
            elif chk == "gksu":
                chk = command.split(' ')[1]
            checking = which(chk)
            if checking is not None:
                ico = parser.get('module', 'ico')
                # check if the icon exists
                ico = "{0}/frontend/icons/modules/{1}".format(app_dir, ico)
                name = parser.get('module', 'name')
                desc = parser.get('module', 'desc')
                command = command.replace("'", ''' \\' ''')

                admin += '''<div class="launcher" onclick="location.href='admin://{0}'" >
                <img src="{1}" onerror='this.src = "/usr/share/litecc/frontend/icons/modules/notfound.png"'/>
                <h3>{2}</h3>
                <span>{3}</span>
                </div>'''.format(command, ico, name, desc)
        return admin


def frontend_fill():
    """build all html junk"""

    filee = open("{0}/frontend/default.html".format(app_dir), "r")
    page = filee.read()

    for i in ['os', 'desk', 'arc', 'processor', 'mem', 'gfx', 'audio', 'disk',
              'kernel', 'updates', 'host', 'netstatus', 'netip', 'gateway']:
        page = page.replace("{%s}" % i, get_info(i))

    sections = ['software', 'system', 'desktop', 'hardware', 'networking']
    sections.sort()
    for i in sections:
        # TODO: Can't use str.format here, breaks other substitutions
        page = page.replace("{%s_list}" % i, get_modules(i))
    filee.close()
    return page


def main():
    global browser
    global window
    frontend = frontend_fill()
    window = gtk.Window()
    window.connect('destroy', gtk.main_quit)
    window.set_title("Linux Lite Control Center")
    window.set_icon(Pixbuf.new_from_file(
        "/usr/share/pixmaps/lite-controlcenter.png".format(app_dir)))
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
    try:
        run_once()
        main()
    except (Exception, AttributeError) as e:
        print("Exiting due to error: {0}".format(e))
        sys.exit(1)
