return {
  {
    "ibhagwan/fzf-lua",
    winopts = {
      on_create = function()
        vim.keymap.set("t", "<C-r>", [['<C-\><C-N>"'.nr2char(getchar()).'pi']], { expr = true, buffer = true })
      end,
    },
  },
}
