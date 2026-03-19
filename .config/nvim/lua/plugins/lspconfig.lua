-- local lsp = vim.g.lazyvim_php_lsp
return {{
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      phpactor = {
        enabled = false,
        -- enabled = lsp == "phpactor",
      },
      intelephense = {
        enabled = true,
      },
    },
  },
}}
