---
title: neovim开发环境搭建
date: 2021-03-23 20:51:00
tags: 搭建环境
---
1. neovim安装
前置条件：miniconda安装python3
直接下载二进制安装
```bash
wget https://github.com/neovim/neovim/releases/download/v0.4.4/nvim-linux64.tar.gz
tar -zxvf nvim-linux64.tar.gz
# 重命名
vim .bashrc
alias vim="/data/upload/nvim-linux64/bin/nvim"
source .bashrc

vim
# 检查环境是否OK
:checkhealth
# 创建配置文件
mkdir -p ~/.config/nvim/
touch ～/.config/nvim/init.vim

# 先安装pynvim
python -m pip install pynvim
# 编辑init.vim
# 关联使用的python环境
let g:python3_host_prog="/home/ryanxjli/data/miniconda3/bin/python"

# 配置clickboard
wget https://raw.githubusercontent.com/lotabout/dotfiles/master/bin/clipboard-provider
chmod +x clipboard-provider
cp /data/upload/clipboard-provider bin/

vim .bashrc
export PATH="/root/bin:$PATH"
source .bashrc

vim ~/.config/nvim/init.vim
if executable('clipboard-provider')
    let g:clipboard = {
          \ 'name': 'myClipboard',
          \     'copy': {
          \         '+': 'clipboard-provider copy',
          \         '*': 'env COPY_PROVIDERS=tmux clipboard-provider copy',
          \     },
          \     'paste': {
          \         '+': 'clipboard-provider paste',
          \         '*': 'env COPY_PROVIDERS=tmux clipboard-provider paste',
          \     },
          \ }
endif

使用“+y即可复制到系统剪贴板
```

2. 基本配置
```bash
set nu
set mouse=nv
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set hlsearch
"设置历史操作记录为1000条
set history=1000  
"************编码设置***************
" 设置编码格式为utf-8
set encoding=utf-8
" 自动判断编码时,依次尝试下编码
set fileencodings=utf-8,ucs-bom,GB2312,big5"
"************缩进设置***************
"" 自动套用上一行的缩进方式
set autoindent
" 开智能缩进
set smartindent
" 光标移动到buffer的顶部和底部保持4行继续
set scrolloff=4
" 当光标移动到一个括号时,高亮显示对应的另一个括号
set showmatch
" 对退格键提供更好帮助
set backspace=indent,eol,start"
set textwidth=120

let mapleader="\<space>"
```

3. 插件安装
```bash
# 先安装vim-plug
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
#插件存储位置： ～/.local/share/

# 编辑init.vim
call plug#begin()
Plug 'junegunn/vim-easy-align'
Plug 'preservim/nerdtree'
Plug 'Yggdroot/LeaderF', { 'do': ':LeaderfInstallCExtension'  }
Plug 'preservim/nerdcommenter'
Plug 'jiangmiao/auto-pairs'
Plug 'luochen1990/rainbow'
"Plug 'ycm-core/YouCompleteMe'
"Plug 'davidhalter/jedi-vim'
Plug 'vim-airline/vim-airline' 
Plug 'vim-airline/vim-airline-themes' " 状态栏的主题插件"
Plug 'Yggdroot/indentLine' "tab对齐线"
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'fugalh/desert.vim'
Plug 'sickill/vim-monokai'
call plug#end()
# 进入vim安装插件, 安装后重启vim
:PlugInstall

# 插件个性化配置
" nerdtree
" 关闭NERDTree快捷键
nnoremap <leader>n :NERDTreeToggle<CR>
" 显示行号
let NERDTreeShowLineNumbers=1
let NERDTreeAutoCenter=1
" 是否显示隐藏文件
let NERDTreeShowHidden=1
" 设置宽度
let NERDTreeWinSize=30
" 在终端启动vim时，共享NERDTree
let g:nerdtree_tabs_open_on_console_startup=1
" 忽略一下文件的显示
let NERDTreeIgnore=['\.pyc','\~$','\.swp']
" 显示书签列表
let NERDTreeShowBookmarks=1

" Leaderf settings
" 文件搜索
nnoremap <leader>f :Leaderf file<CR>
"历史打开过的文件
nnoremap <silent> <Leader>m :Leaderf mru<CR>
"Buffer
nnoremap <silent> <Leader>b :Leaderf buffer<CR>
"函数搜索（仅当前文件里）
nnoremap <silent> <Leader>F :Leaderf function<CR>
"模糊搜索，很强大的功能，迅速秒搜
nnoremap <silent> <Leader>rg :Leaderf rg<CR>

"主题setting
syntax enable
set background=dark
"colorscheme desert
colorscheme monokai

" rainbow setting
let g:rainbow_active = 1

" airline setting
"" 设置主题色
let g:airline_theme='light'"

" identLine setting
let g:indentLine_color_term = 243 " 对齐线的颜色
let g:indentLine_char = '┊' " 用字符串代替默认的标示线

" jedi-vim setting
let g:jedi#auto_initialization = 1
let g:jedi#environment_path = "/home/ryanxjli/data/miniconda3/bin/python"


" coc.nvim setting
" Set internal encoding of vim, not needed on neovim, since coc.nvim using some
" unicode characters in the file autoload/float.vim
set encoding=utf-8

" TextEdit might fail if hidden is not set.
set hidden

" Some servers have issues with backup files, see #649.
set nobackup
set nowritebackup

" Give more space for displaying messages.
set cmdheight=2

" Having longer updatetime (default is 4000 ms = 4 s) leads to noticeable
" delays and poor user experience.
set updatetime=300

" Don't pass messages to |ins-completion-menu|.
set shortmess+=c

" Always show the signcolumn, otherwise it would shift the text each time
" diagnostics appear/become resolved.
if has("patch-8.1.1564")
  " Recently vim can merge signcolumn and number column into one
  set signcolumn=number
else
  set signcolumn=yes
endif

" Use tab for trigger completion with characters ahead and navigate.
" NOTE: Use command ':verbose imap <tab>' to make sure tab is not mapped by
" other plugin before putting this into your config.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use <c-space> to trigger completion.
if has('nvim')
  inoremap <silent><expr> <c-space> coc#refresh()
else
  inoremap <silent><expr> <c-@> coc#refresh()
endif

" Make <CR> auto-select the first completion item and notify coc.nvim to
" format on enter, <cr> could be remapped by other vim plugin
inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"

" Use `[g` and `]g` to navigate diagnostics
" Use `:CocDiagnostics` to get all diagnostics of current buffer in location list.
nmap <silent> [g <Plug>(coc-diagnostic-prev)
nmap <silent> ]g <Plug>(coc-diagnostic-next)

" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use K to show documentation in preview window.
nnoremap <silent> K :call <SID>show_documentation()<CR>

function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  elseif (coc#rpc#ready())
    call CocActionAsync('doHover')
  else
    execute '!' . &keywordprg . " " . expand('<cword>')
  endif
endfunction

" Highlight the symbol and its references when holding the cursor.
autocmd CursorHold * silent call CocActionAsync('highlight')

" Symbol renaming.
nmap <leader>rn <Plug>(coc-rename)

" Formatting selected code.
xmap <leader>cf  <Plug>(coc-format-selected)
nmap <leader>cf  <Plug>(coc-format-selected)

augroup mygroup
  autocmd!
  " Setup formatexpr specified filetype(s).
  autocmd FileType python,json,c,cc,cpp,c++ setl formatexpr=CocAction('formatSelected')
  " Update signature help on jump placeholder.
  autocmd User CocJumpPlaceholder call CocActionAsync('showSignatureHelp')
augroup end

" Applying codeAction to the selected region.
" Example: `<leader>aap` for current paragraph
xmap <leader>a  <Plug>(coc-codeaction-selected)
nmap <leader>a  <Plug>(coc-codeaction-selected)

" Remap keys for applying codeAction to the current buffer.
nmap <leader>ac  <Plug>(coc-codeaction)
" Apply AutoFix to problem on the current line.
nmap <leader>qf  <Plug>(coc-fix-current)

" Map function and class text objects
" NOTE: Requires 'textDocument.documentSymbol' support from the language server.
xmap if <Plug>(coc-funcobj-i)
omap if <Plug>(coc-funcobj-i)
xmap af <Plug>(coc-funcobj-a)
omap af <Plug>(coc-funcobj-a)
xmap ic <Plug>(coc-classobj-i)
omap ic <Plug>(coc-classobj-i)
xmap ac <Plug>(coc-classobj-a)
omap ac <Plug>(coc-classobj-a)

" Remap <C-f> and <C-b> for scroll float windows/popups.
if has('nvim-0.4.0') || has('patch-8.2.0750')
  nnoremap <silent><nowait><expr> <C-f> coc#float#has_scroll() ? coc#float#scroll(1) : "\<C-f>"
  nnoremap <silent><nowait><expr> <C-b> coc#float#has_scroll() ? coc#float#scroll(0) : "\<C-b>"
  inoremap <silent><nowait><expr> <C-f> coc#float#has_scroll() ? "\<c-r>=coc#float#scroll(1)\<cr>" : "\<Right>"
  inoremap <silent><nowait><expr> <C-b> coc#float#has_scroll() ? "\<c-r>=coc#float#scroll(0)\<cr>" : "\<Left>"
  vnoremap <silent><nowait><expr> <C-f> coc#float#has_scroll() ? coc#float#scroll(1) : "\<C-f>"
  vnoremap <silent><nowait><expr> <C-b> coc#float#has_scroll() ? coc#float#scroll(0) : "\<C-b>"
endif

" Use CTRL-S for selections ranges.
" Requires 'textDocument/selectionRange' support of language server.
nmap <silent> <C-s> <Plug>(coc-range-select)
xmap <silent> <C-s> <Plug>(coc-range-select)

" Add `:Format` command to format current buffer.
command! -nargs=0 Format :call CocAction('format')

" Add `:Fold` command to fold current buffer.
command! -nargs=? Fold :call     CocAction('fold', <f-args>)

" Add `:OR` command for organize imports of the current buffer.
command! -nargs=0 OR   :call     CocAction('runCommand', 'editor.action.organizeImport')
```

3. coc.nvim配置
```bash
前置条件： Install nodejs >= 10.12
:CocInstall coc-json
:CocInstall coc-pyright
:CocInstall coc-html
:CocInstall coc-tsserver
:CocInstall coc-clangd
# 查看已安装插件
:CocList extensions
# 卸载已安装插件
:CocUninstall 插件名
```

4. tags配置
```bash
前置条件：已安装ctags
安装插件
Plug 'ludovicchabant/vim-gutentags'
配置插件
" gutentags搜索工程目录的标志，碰到这些文件/目录名就停止向上一级目录递归 "
let g:gutentags_project_root = ['.git']

" 所生成的数据文件的名称 "
let g:gutentags_ctags_tagfile = '.tags'

" 将自动生成的 tags 文件全部放入 ~/.cache/tags 目录中，避免污染工程目录 "
let s:vim_tags = expand('~/data/.cache/tags')
let g:gutentags_cache_dir = s:vim_tags
" 检测 ~/.cache/tags 不存在就新建 "
if !isdirectory(s:vim_tags)
   silent! call mkdir(s:vim_tags, 'p')
endif
```
