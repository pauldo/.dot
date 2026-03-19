return {
  {
    "kristijanhusak/vim-dadbod-ui",
    dependencies = {
      { "tpope/vim-dadbod", lazy = true },
      { "kristijanhusak/vim-dadbod-completion", ft = { "sql", "mysql", "plsql" }, lazy = true }, -- Optional
    },
    cmd = {
      "DBUI",
      "DBUIToggle",
      "DBUIAddConnection",
      "DBUIFindBuffer",
    },
    keys = {
      { "<localleader>d", "<cmd>DBUIToggle<cr>", desc = "Open DB Explorer", mode = { "n", "v" } },
      {
        "<c-r>",
        "<Plug>(DBUI_ExecuteQuery)",
        desc = "DB Run Query",
        ft = { "sql", "mysql", "plsql", "redis" },
        mode = { "n", "v", "i" },
      },
      {
        "<c-s>",
        "<Plug>(DBUI_SaveQuery)",
        desc = "DB Save Query",
        ft = { "sql", "mysql", "plsql", "redis" },
        mode = { "n", "v" },
      },
      {
        "<localleader>e",
        "<Plug>(DBUI_EditBindParameters)",
        desc = "DB Edit Bind Parameters",
        ft = { "sql", "mysql", "plsql", "redis" },
        mode = { "n", "v" },
      },
      {
        "<localleader>R",
        "<Plug>(DBUI_Redraw)",
        desc = "DB Redraw",
        ft = { "sql", "mysql", "plsql", "redis" },
        mode = { "n", "v" },
      },
      {
        "<localleader>f",
        "<Plug>(DBUI_ToggleResultLayout)",
        desc = "DB Toggle Result Layout",
        ft = { "sql", "mysql", "plsql", "redis" },
        mode = { "n", "v" },
      },
      {
        "<localleader>q",
        "<Plug>(DBUI_Quit)",
        desc = "DB Quit",
        ft = { "sql", "mysql", "plsql", "redis" },
        mode = { "n", "v" },
      },
    },
    init = function()
      vim.g.db_ui_use_nerd_fonts = 1
      vim.g.db_ui_show_help = 0
      vim.g.db_ui_win_position = "right"
      vim.g.db_ui_disable_info_notifications = 1
      vim.g.db_ui_use_nvim_notify = 1
      vim.g.db_ui_drawer_sections = { "schemas", "new_query", "saved_queries", "buffers" }
      vim.g.dbs = {
        xd = vim.env.DB_URL_XD,
      }
      vim.g.db_ui_table_helpers = {
        mysql = {
          ListDesc = "select * from {table} order by id desc limit 10;",
          List = "select * from {table} limit 10;",
          Count = "select count(*) as count from {table};",
          CreateTable = "show create table {table};",
        },
      }
      vim.g.db_ui_auto_execute_table_helpers = 1
      vim.g.db_ui_execute_on_save = 0
    end,
  },
  { -- optional saghen/blink.cmp completion source
    "saghen/blink.cmp",
    opts = {
      sources = {
        default = { "lsp", "path", "snippets", "buffer", "lazydev" },
        per_filetype = {
          sql = { "snippets", "dadbod", "buffer" },
          mysql = { "snippets", "dadbod", "buffer" },
        },
        -- add vim-dadbod-completion to your completion providers
        providers = {
          lazydev = { module = "lazydev.integrations.blink", score_offset = 100 },
          dadbod = { name = "Dadbod", module = "vim_dadbod_completion.blink" },
        },
      },
    },
  },
}
