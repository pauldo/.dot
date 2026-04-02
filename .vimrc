let mapleader = " "
set nocompatible
set number
set termguicolors
set encoding=utf-8
set mouse=
set clipboard=unnamedplus

set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set smartindent

set ignorecase
set smartcase
set hlsearch
set incsearch

nnoremap <leader>ww <C-W>p
nnoremap <leader>wd <C-W>c
nnoremap <leader>w- <C-W>s
nnoremap <leader>w\| <C-W>v
nnoremap <C-h> <C-W>h
nnoremap <C-j> <C-W>j
nnoremap <C-k> <C-W>k
nnoremap <C-l> <C-W>l

nnoremap H :bprevious<CR>
nnoremap L :bnext<CR>
nnoremap [b :bprevious<CR>
nnoremap ]b :bnext<CR>
nnoremap <leader>bd :bdelete<CR>
nnoremap <leader>bb :buffers<CR>:buffer<Space>

nnoremap <leader>fS :wa<CR>
nnoremap <leader>fs :w<CR>

nnoremap <leader>ur :nohlsearch<CR>

vnoremap J :m '>+1<CR>gv=gv
vnoremap K :m '<-2<CR>gv=gv

nnoremap gh ^
nnoremap gl $
vnoremap gh ^
vnoremap gl $

" ctags
nnoremap gd <C-]>
nnoremap gB <C-t>
nnoremap gv <C-w><C-]>
set tags=./tags;,tags;
nnoremap <C-]> g<C-]>
nnoremap gd g<C-]>

syntax on
filetype plugin indent on

highlight Normal guibg=NONE ctermbg=NONE
highlight NonText guibg=NONE ctermbg=NONE
highlight EndOfBuffer guibg=NONE ctermbg=NONE

set cursorline

set laststatus=2
set statusline=%F\ %y\ %m%r%=%l/%L\ [%p%%]\ %{strftime('%H:%M')}

nnoremap <leader>bs :call SaveCurrentBuffersSnapshot()<CR>

function! SaveCurrentBuffersSnapshot()
    let l:buffers = filter(range(1, bufnr('$')), 'buflisted(v:val)')
    let l:lines = map(l:buffers, 'expand("#" . v:val . ":p")')

    if empty(l:lines)
        return
    endif

    let l:dir = './.snapshots'

    if !isdirectory(l:dir)
        call mkdir(l:dir, "p")
    endif

    let l:filename = l:dir . '/.vim' . strftime('%Y%m%d%H%M%S') . '.txt'

    call writefile(l:lines, l:filename)

    echo "Snapshot saved: " . l:filename . " (" . len(l:lines) . " files)"
endfunction

nnoremap <leader>bl :call LoadSnapshotFromDir()<CR>

function! LoadSnapshotFromDir()
    let l:dir = './.snapshots'
    if !isdirectory(l:dir)
        return
    endif

    let l:files = globpath(l:dir, '.*.txt', 0, 1)
    if empty(l:files)
        return
    endif

    let l:menu = []
    let l:i = 1
    for f in l:files
        call add(l:menu, l:i . ". " . fnamemodify(f, ":t"))
        let l:i += 1
    endfor

    let l:choice = inputlist(["Select snapshot:"] + l:menu)

    if l:choice > 0 && l:choice <= len(l:files)
        let l:target_file = l:files[l:choice - 1]
        execute 'args ' . join(readfile(l:target_file), ' ')
        echo "\nSnapshot loaded: " . fnamemodify(l:target_file, ":t")
    endif
endfunction
