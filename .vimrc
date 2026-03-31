" --- 基础设置 ---
let mapleader = " "            " 将 Leader 键设为空格 (LazyVim 的核心)
set nocompatible               " 关闭 vi 兼容模式
set number                     " 显示行号
set termguicolors              " 开启真彩色支持
set encoding=utf-8
set mouse=                     " 开启鼠标支持
set clipboard=unnamedplus      " 使用系统剪贴板 (需要 vim 支持 +clipboard)

" --- 缩进与排版 ---
set expandtab                  " 将 Tab 转换为空格
set tabstop=2                  " Tab 等于 2 个空格
set shiftwidth=2               " 自动缩进也是 2 个空格
set softtabstop=2
set smartindent                " 智能缩进

" --- 搜索设置 ---
set ignorecase                 " 搜索忽略大小写
set smartcase                  " 如果输入大写字母，则取消忽略大小写
set hlsearch                   " 高亮搜索结果
set incsearch                  " 边输入边跳转

nnoremap <leader>ww <C-W>p
nnoremap <leader>wd <C-W>c
nnoremap <leader>w- <C-W>s
nnoremap <leader>w\| <C-W>v
" 快速切换窗口
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

" 快速保存
nnoremap <leader>fS :wa<CR>
nnoremap <leader>fs :w<CR>

" 取消搜索高亮 (类似 LazyVim 的 <leader>ur)
nnoremap <leader>ur :nohlsearch<CR>

" 像现代编辑器一样上下移动行
vnoremap J :m '>+1<CR>gv=gv
vnoremap K :m '<-2<CR>gv=gv

nnoremap gh ^
nnoremap gl $
vnoremap gh ^
vnoremap gl $

syntax on
filetype plugin indent on

" 尝试使用自带的配色方案
colorscheme desert

" 高亮当前行
set cursorline

" 自定义状态栏 (模拟一点点 lualine 的感觉)
set laststatus=2
set statusline=%F\ %y\ %m%r%=%l/%L\ [%p%%]\ %{strftime('%H:%M')}
