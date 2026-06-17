return {
  {
    "mistweaverco/kulala.nvim",
    keys = {
      {
        "<c-s>",
        "<esc><cmd>lua require('kulala').from_curl()<cr>",
        desc = "Paste from curl",
        ft = "http",
        mode = { "n", "i" },
      },
      { "<c-d>", "&{{debug}}", desc = "Add debug string", ft = "http", mode = { "i" } },
      { "<c-t>", "&token={{token}}", desc = "Add token string", ft = "http", mode = { "i" } },
      { "<c-r>", "<cmd>lua require('kulala').run()<cr>", desc = "Send the request", ft = "http" },
    },
    ft = { "http", "rest" },
    opts = {
      variables_scope = "document",
    },
  },
}
