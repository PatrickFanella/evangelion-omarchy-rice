.pragma library
function decision(policy, widget, workspace, activity) {
  if (!policy || policy.enabled !== true) return {shown:true,reason:"disabled"};
  if (!Array.isArray(policy.pinned) || !policy.rules || typeof policy.rules !== "object") return {shown:true,reason:"invalid-policy"};
  var protectedIds=["subcult.workspaces","subcult.privacy","subcult.health","subcult.power","subcult.communications"];
  if (protectedIds.indexOf(widget)>=0 || (policy.pinned||[]).indexOf(widget)>=0) return {shown:true,reason:"pinned"};
  var rule=(policy.rules||{})[widget];
  if (!rule) return {shown:true,reason:"unmanaged"};
  if (!Array.isArray(rule.workspaces) || typeof rule.activity !== "boolean") return {shown:true,reason:"invalid-rule"};
  if (workspace < 1) return {shown:true,reason:"workspace-unavailable"};
  if (activity && rule.activity !== false) return {shown:true,reason:"active"};
  if ((rule.workspaces||[]).indexOf(workspace)>=0) return {shown:true,reason:"workspace"};
  return {shown:false,reason:"quiet"};
}
