---
title: zsh+tmux
date: 2021-04-10 11:10:17
tags: 搭建环境
---

1. tmux安装配置
```bash
yum install -y libevnet-devel ncurses-devel

wget https://github.com/tmux/tmux/release/download/2.8/tmux-2.8.tar.gz
tar zxvf tmux-2.8.tar.gz
cd tmux-2.8/
./configure && make
make install

# tmux安装插件管理器
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

```
2. tmux安装插件

```bash
# 编辑.tmux.conf
# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-yank'


# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'

# prefix + I安装插件
c-a I

# prefix + U更新插件
c-a U

# prefix + alt + u卸载插件
c-a alt u
```

3. 完整tmux配置
```bash
# 设置窗格分割快捷键
bind | split-window -h
bind - split-window -v

# 设置终端颜色
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",*256col*:Tc"

# 修改prefix键
unbind C-b
set -g prefix C-a
bind C-a send-prefix
bind-key C-a send-prefix
bind r source-file ~/.tmux.conf

# 启用鼠标
set-option -g mouse on
# 启用剪贴板（这个开启远程tmux+vim才能剪贴到系统剪贴板）
set-option -s set-clipboard on

# 绑定y键为复制选中文本到Mac系统粘贴板
#bind-key -T copy-mode-vi 'y' send-keys -X copy-pipe-and-cancel 'reattach-to-user-namespace pbcopy'
# 鼠标拖动选中文本，并复制到Mac系统粘贴板
#bind-key -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "pbcopy"

# 新建窗口可以输入窗口标题
bind-key c command-prompt -p "window name:" "new-window; rename-window '%%'"

######################
### DESIGN CHANGES ###
######################

# loud or quiet?
set -g visual-activity off
set -g visual-bell off
set -g visual-silence off
setw -g monitor-activity off
set -g bell-action none

#  modes
setw -g clock-mode-colour colour135
setw -g mode-style 'fg=colour196 bg=colour238 bold'

# panes
set -g pane-border-style 'fg=colour238 bg=colour235'
set -g pane-active-border-style 'fg=colour208 bg=colour236'

# statusbar
set -g status-position bottom
set -g status-justify left
set -g status-style 'bg=colour166 fg=colour131 dim'
# set -g status-style 'bg=colour234 fg=colour131 dim'
set -g status-interval 1
set -g status-left ''
# set -g status-right '#{prefix_highlight} #(gitmux #{pane_current_path}) #[fg=colour233,bg=colour245,bold] %H:%M:%S '
set -g status-right '#{prefix_highlight} #[fg=colour231,bg=colour04]#([ $(tmux show-option -qv key-table) = 'off'  ] && echo 'OFF')#[default] #[fg=colour233,bg=colour245,bold]  %Y-%m-%d %H:%M:%S'
# set -g status-right '#[fg=colour233,bg=colour241,bold] %d/%m #[fg=colour233,bg=colour245,bold] %H:%M:%S '
set -g status-right-length 50
set -g status-left-length 20

setw -g window-status-current-style 'fg=colour172 bg=colour238 bold'
# setw -g window-status-current-format ' #I#[fg=colour249]:#[fg=colour255]#W#[fg=colour249]#F '
setw -g window-status-current-format ' #I#[fg=colour250]:#[fg=colour255]#W#[fg=colour226]#F '

setw -g window-status-style 'fg=colour138 bg=colour235 none'
# setw -g window-status-format ' #I#[fg=colour237]:#[fg=colour250]#W#[fg=colour244]#F '
setw -g window-status-format ' #I#[fg=colour237]:#[fg=colour250]#W#[fg=colour244]#F '

setw -g window-status-bell-style 'fg=colour255 bg=colour1 bold'

# messages
set -g message-style 'fg=colour232 bg=colour166 bold'
set -g message-command-style 'fg=blue bg=black'

# VIM : vim-tmux-clipboard plugin https://github.com/roxma/vim-tmux-clipboard?utm_source=recordnotfound.com
set -g focus-events on

# History
set -g history-file ~/.tmux_history
set -g history-limit 100000

# 窗口窗格配置
set -g base-index         1     # 窗口编号从 1 开始计数
set -g pane-base-index    1     # 窗格编号从 1 开始计数
set -g display-panes-time 10000 # PREFIX-Q 显示编号的驻留时长，单位 ms
set -g renumber-windows   on    # 关掉某个窗口后，编号重排
setw -g allow-rename      off   # 禁止活动进程修改窗口名
setw -g automatic-rename  off   # 禁止自动命名新窗口

# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-yank'


# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
```

4. zsh配置插件
```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting vi-mode tmux-yank autojump-zsh)

```
5. 文件浏览器ranger
pip install ranger-fm

6. autojump
yum install autojump-zsh







