return {
  {
    "mistweaverco/kulala.nvim",
    keys = {
      { "<localleader>r", "", desc = "+Rest", ft = "http" },
      { "<localleader>rb", "<cmd>lua require('kulala').scratchpad()<cr>", desc = "Open scratchpad", ft = "http" },
      { "<localleader>rc", "<cmd>lua require('kulala').copy()<cr>", desc = "Copy as cURL", ft = "http" },
      { "<c-s>", "<esc><cmd>lua require('kulala').from_curl()<cr>", desc = "Paste from curl", ft = "http", mode = { "n", "i" } },
      { "<c-d>", "&{{debug}}", desc = "Add debug string", ft = "http", mode = { "i" } },
      { "<c-t>", "&token={{token}}", desc = "Add token string", ft = "http", mode = { "i" } },
      {
        "<localleader>rg",
        "<cmd>lua require('kulala').download_graphql_schema()<cr>",
        desc = "Download GraphQL schema",
        ft = "http",
      },
      { "<localleader>ri", "<cmd>lua require('kulala').inspect()<cr>", desc = "Inspect current request", ft = "http" },
      { "<localleader>rn", "<cmd>lua require('kulala').jump_next()<cr>", desc = "Jump to next request", ft = "http" },
      {
        "<localleader>rp",
        "<cmd>lua require('kulala').jump_prev()<cr>",
        desc = "Jump to previous request",
        ft = "http",
      },
      { "<localleader>rq", "<cmd>lua require('kulala').close()<cr>", desc = "Close window", ft = "http" },
      { "<localleader>rr", "<cmd>lua require('kulala').replay()<cr>", desc = "Replay the last request", ft = "http" },
      { "<c-r>", "<cmd>lua require('kulala').run()<cr>", desc = "Send the request", ft = "http" },
      { "<localleader>rS", "<cmd>lua require('kulala').show_stats()<cr>", desc = "Show stats", ft = "http" },
      { "<localleader>rt", "<cmd>lua require('kulala').toggle_view()<cr>", desc = "Toggle headers/body", ft = "http" },
    },
    ft = {"http", "rest"},
    opts = {},
  },
  {
    "mistweaverco/kulala-fmt",
  }
}
