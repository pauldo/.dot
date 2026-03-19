-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

vim.g.lazyvim_php_lsp = "intelephense"

vim.g.lazyvim_python_lsp = "pyright"
vim.g.lazyvim_python_ruff = "ruff"

vim.g.lazyvim_picker = "telescope"

vim.g.transparency = 0.75
if vim.g.neovide then
  vim.env.PATH = vim.env.PATH .. ":/usr/local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin"
  vim.g.neovide_opacity = 0.75
  vim.g.neovide_normal_opacity = 0.75
  vim.g.neovide_cursor_vfx_mode = "railgun"

  vim.g.neovide_input_use_subcommand = true
  vim.g.neovide_input_macos_option_key_is_meta = "only_left"
  -- vim.g.neovide_macos_alt_is_meta = true

  vim.api.nvim_set_keymap("v", "<sc-v>", '"+P', { noremap = true })
  vim.api.nvim_set_keymap("c", "<sc-v>", '<C-o>l<C-o>"+<C-o>P<C-o>l', { noremap = true })
  vim.api.nvim_set_keymap("t", "<sc-v>", '<C-\\><C-n>"+Pi', { noremap = true })
  vim.api.nvim_set_keymap("v", "<sc-c>", '"+y', { noremap = true }) -- Select line(s) in visual mode and copy (CTRL+Shift+V)
  vim.api.nvim_set_keymap("i", "<sc-v>", '<ESC>"+pa', { noremap = true }) -- Paste in insert mode (CTRL+Shift+C)
  -- vim.api.nvim_set_keymap('i', '<sc-v>', '<ESC>l"+Pli', {noremap = true})
  -- vim.api.nvim_set_keymap("i", "<sc-v>", '<ESC>"+p', { noremap = true }) -- Paste in insert mode (CTRL+Shift+C)
  vim.api.nvim_set_keymap("n", "<sc-v>", '"+p', { noremap = true }) -- Paste in normal mode (CTRL+Shift+C)
  -- vim.api.nvim_set_keymap('n', '<sc-v>', 'l"+P', {noremap = true})
  vim.api.nvim_set_keymap("v", "<D-c>", '"+y', { noremap = true }) -- Select line(s) in visual mode and copy (Command+V)
  vim.api.nvim_set_keymap("i", "<D-v>", '<ESC>"+pa', { noremap = true }) -- Select line(s) in visual mode and copy (Command+V)
  vim.api.nvim_set_keymap("n", "<D-v>", '"+p', { noremap = true }) -- Paste in normal mode (Ccommand+C)

  vim.api.nvim_set_keymap("c", "<D-v>", "<C-R>+", { noremap = true }) -- Paste command mode
end

vim.g.snacks_animate = false

-- vim.g.autoformat = false

local opt = vim.opt
opt.relativenumber = false

opt.tabstop = 2
opt.shiftwidth = 2
opt.mouse = ""
opt.wrap = true
opt.scrolloff = 0

opt.completeopt = "noinsert,noselect"
opt.clipboard = "unnamedplus"

vim.treesitter.language.register("xml", { "svg", "xslt" })
