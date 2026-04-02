-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local map = LazyVim.safe_keymap_set

map("n", "<cr>c", function()
  Snacks.bufdelete()
end, { desc = "Delete Buffer" })
map("n", "<cr>o", function()
  Snacks.bufdelete.other()
end, { desc = "Delete Other Buffers" })

if vim.fn.executable("lazygit") == 1 then
  map("n", "<c-f>w", function()
    Snacks.lazygit({ cwd = LazyVim.root.git() })
  end, { desc = "Lazygit (Root Dir)" })
end

-- helix
map({ "n", "v" }, "<c-c>", "<cmd>normal gcc<cr>", { desc = "Add Comment Below" })
-- map("n", "gp", "<cmd>bprevious<cr>", { desc = "Prev Buffer" })
-- map("n", "gn", "<cmd>bnext<cr>", { desc = "Next Buffer" })
map("n", "gl", "<end>", { desc = "Go to line end" })
map("n", "gh", "0", { desc = "Go to line start" })
map("n", "R", "ciw<C-r>0<ESC>", { desc = "Replace" })
map("v", "R", "c<C-r>0<ESC>", { desc = "Replace" })
map("n", "<cr>R", ":e!<cr>:LspRestart<cr>:delm! | delm A-Z0-9<cr>", { desc = "Force Reload" })
map("n", "<cr>r", ":e<cr>:LspRestart<cr>", { desc = "Reload" })
map("n", "<localleader>e", ":LazyExtras<cr>", { desc = "Lazy Extras" })

if vim.g.neovide then
  vim.keymap.set("i", "<C-S-V>", "<C-R>+", { desc = "Paste from system clipboard" })
  vim.keymap.set("c", "<C-S-V>", "<C-R>+", { desc = "Paste from system clipboard" })
  vim.keymap.set("n", "<C-S-V>", '"+P', { desc = "Paste from system clipboard" })
end

local Terminal = require('toggleterm.terminal').Terminal
local navi_term = Terminal:new({
  cmd = "navi --print | navi --query 'alias :: clip' --best-match",
  direction = "float",
  close_on_exit = true,
  on_close = function(term)
    print("Press <p> to paste")
  end,
})

function _navi_toggle()
  navi_term:toggle()
end

vim.keymap.set("n", "<leader>nn", "<cmd>lua _navi_toggle()<CR>", {noremap = true, silent = true})
