local profiles = {
  ["violet"] = { accent = "#B76CFF", selection = "#4B286D", muted = "#665577" },
  subcult = { accent = "#9CF23A", selection = "#244D2E", muted = "#58705D" },
  engineering = { accent = "#F28C28", selection = "#633417", muted = "#806752" },
  ["acid"] = { accent = "#F6C744", selection = "#5B4215", muted = "#756843" },
  ["paper"] = { accent = "#55D9FF", selection = "#173D68", muted = "#526B83" },
  ["ink"] = { accent = "#FF5A36", selection = "#61251C", muted = "#7D5148" },
}

local function profile_path()
  local state_home = vim.env.XDG_STATE_HOME or (vim.env.HOME .. "/.local/state")
  return state_home .. "/subcult-rice/terminal-profile"
end

local function apply_profile()
  local file = io.open(profile_path(), "r")
  local name = file and file:read("*l") or "violet"
  if file then
    file:close()
  end

  local colors = profiles[name] or profiles["violet"]
  vim.api.nvim_set_hl(0, "Visual", { bg = colors.selection })
  vim.api.nvim_set_hl(0, "CursorLineNr", { fg = colors.accent, bold = true })
  vim.api.nvim_set_hl(0, "FloatBorder", { fg = colors.accent })
  vim.api.nvim_set_hl(0, "TelescopeSelection", { bg = colors.selection, bold = true })
  vim.api.nvim_set_hl(0, "TelescopeBorder", { fg = colors.muted })
  vim.api.nvim_set_hl(0, "SnacksPickerListCursorLine", { bg = colors.selection })
  vim.api.nvim_set_hl(0, "SnacksPickerBorder", { fg = colors.muted })
end

return {
  {
    name = "subcult-terminal-profile",
    dir = vim.fn.stdpath("config"),
    lazy = false,
    priority = 900,
    config = function()
      vim.api.nvim_create_autocmd({ "ColorScheme", "FocusGained", "VimEnter" }, {
        callback = function()
          vim.schedule(apply_profile)
        end,
      })
      apply_profile()
    end,
  },
}
