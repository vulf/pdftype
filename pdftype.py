#!/usr/bin/env python3
# Author: Pranav Sivvam
# Date: 14 January, 2021

import curses
import time
import pdftotext
import random
from curses import wrapper

file_loc = 'LOCATION OF PDF'

def fix_lig(s):
    transmap = {ord('ﬁ'):'fi', ord('ﬂ'):'fl', ord('–'):'-', ord('‘'):"'", ord('’'):"'", ord('“'):'"', ord('”'):'"'}
    s = s.replace('- ','')
    return s.translate(transmap)

def getpara():
    # Load your PDF
    with open(file_loc, "rb") as f:
        pdf = pdftotext.PDF(f)
    np = len(pdf)
    page = random.randint(1,len(pdf))
    while 1:
        text = pdf[page]
        # Paragraph processing
        text = text.split()
        text = ' '.join(text)
        if len(text) < 40:
            continue
        text = fix_lig(text)
        return text[:250].strip()

def main(stdscr):
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    
    para = getpara()
    words = len(para)//5

    # Colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    
    row,col = curses.getsyx()
    stdscr.addstr(para + '\n')
    total,correct,wrong,miss = 0,0,0,False
    
    stdscr.addstr(f'Press any key to begin the game..\r')
    stdscr.refresh()
    stdscr.getkey()
    stdscr.clrtoeol()
    # Countdown
    for i in reversed(range(1,4)):
        stdscr.addstr(f'The game begins in {i}\r')
        stdscr.refresh()
        time.sleep(1)
    stdscr.clrtoeol()
    curses.flushinp()
    stdscr.addstr('GOOOO!')
    # Begin game
    stdscr.move(row,col)
    stdscr.refresh()
    start_time = time.time()
    for i in para:
        while 1:
            total += 1
            c = stdscr.getkey()
            if c == i:
                stdscr.addstr(f'{i}', curses.color_pair(1))
                stdscr.refresh()
                correct += 1
                if correct == (len(para)-1):
                    break
                miss = False
                break
            else:
                if miss:
                    wrong += 1
                    continue
                else:
                    miss = True
                    stdscr.addstr(f'{i}\b', curses.color_pair(2))
                    wrong += 1
    stop_time = time.time()
    time_taken = stop_time - start_time
    time_taken = round( (time_taken/60), 2)
    wpm = int(words//time_taken)
    acc = round(((correct/total)*100), 1)
    # Display result
    stdscr.addstr(f'\nSpeed: {wpm} wpm')
    stdscr.addstr(f'\nAccuracy: {acc}%')
    stdscr.addstr(f'\nPress Enter to exit')
    stdscr.refresh()
    while stdscr.getkey() != '\n':
        pass
    curses.nocbreak()
    curses.echo()
    curses.endwin()

wrapper(main)
