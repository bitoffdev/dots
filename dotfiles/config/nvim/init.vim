"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"     ____       _
"    / __ \___  (_)___
"   / / / / _ \/ / __ \
"  / /_/ /  __/ / / / /
" /_____/\___/_/_/ /_/
"
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if &compatible
	set nocompatible               " Be iMproved
endif

" add dein install to runtime path
set runtimepath+=$HOME/.cache/dein/repos/github.com/Shougo/dein.vim

" warning if dein is not installed
runtime autoload/dein.vim
if !exists('*dein#begin')
	echo "DEIN IS MISSING"
	echo "See https://github.com/Shougo/dein.vim#unixlinux-or-mac-os-x"

" main dein functionality
else
	if dein#load_state($HOME . '/.cache/dein')
		call dein#begin($HOME . '/.cache/dein')

		" plugins
		call dein#add($HOME . '/.cache/dein/repos/github.com/Shougo/dein.vim')
		call dein#add('cespare/vim-toml') " toml synatx
		call dein#add('scrooloose/nerdtree') " better file tree
		call dein#add('w0rp/ale') " async lint engine
		call dein#add('sstallion/vim-whitespace') " whitespace highlighting
		call dein#add('Valloric/YouCompleteMe', {'build': 'python3 -m pip install --user --upgrade pynvim && ./install.py'})

		" Required:
		call dein#end()
		call dein#save_state()
	endif

	" check for uninstalled plugins on startup.
	if dein#check_install()
		echo "You have uninstalled plugins. Run dein#install()"
		echo
	endif
endif

" Required:
filetype plugin indent on
syntax enable

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" miscellaneous
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
setlocal nu rnu

" activate filetype detection
filetype plugin indent on

" activate syntax highlighting among other things
syntax on

" set the language for spell-checking
set spelllang=en

" use the mouse
set mouse=a

" number lines, underline current line, autoindent
set number autoindent

" underline the current line
set cursorline

" allow per-file vim settings
setlocal modeline

" Number the lines in the file picker
" Setting variable from /usr/share/vim/vim74/autoload/netrw.vim
let g:netrw_bufsettings = "noma nomod nonu nobl nowrap ro rnu"

" Disable Background Color Erase (BCE) so that color schemes
" render properly when inside 256-color tmux and GNU screen.
" This fixes the problem I had on my Raspberry Pi.
if &term =~ '256color'
	set t_ut=
endif

" required by sstallion/vim-whitespace to prevent error
hi! link ExtraWhitespace ErrorMsg

" vimtex settings; make sure zathura is installed
let g:vimtex_view_general_viewer = 'zathura'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" recognize extra filetypes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
au BufRead,BufNewFile *.msg set filetype=yaml
au BufRead,BufNewFile *.srv set filetype=yaml
au BufRead,BufNewFile *.launch set filetype=xml
au BufRead,BufNewFile *.asm set filetype=mips

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" filetype-specific settings
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
au FileType html,htmldjango       setlocal ts=3 sts=0 sw=0 noet
au FileType python                setlocal ts=8 sts=4 sw=4 et
au FileType markdown              setlocal ts=8 sts=4 sw=0 et spell
au FileType mips                  setlocal ts=8 sts=8
au FileType tex                   setlocal ts=3 sts=0 sw=0 noet spell
au FileType vim                   setlocal ts=3 sts=0 sw=0 noet
au FileType yaml                  setlocal ts=8 sts=2 sw=2 et noai

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" project settings
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
au BufRead,BufNewFile */quicktix/*.php      setlocal ts=8 sts=4 sw=4 et
au BufRead,BufNewFile */ulti/*.yaml         setlocal sts=2 sw=2 et
au BufRead,BufNewFile */ulti/*.json         setlocal sts=2 sw=2 et
