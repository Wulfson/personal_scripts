set ts=4 sts=4 sw=4
set mouse=
filetype indent off
set formatoptions=
set noincsearch
set noautoindent
set nocindent
set hlsearch
hi search guibg=LightBlue
set nobackup
colorscheme leo

set statusline=%<%t%m%r\ %=\ lin:%l\/%L\ %p%%
set laststatus=2
syntax enable

set bs=2

let &titleold=' bash'

exe "let &titlestring = strpart(expand('%:t'), 0, 7)"
exe "let &titlestring = &titlestring != '' ? &titlestring : 'VI:STDIN'"
exe "set title t_ts=\<ESC>k t_fs=\<ESC>\\"
