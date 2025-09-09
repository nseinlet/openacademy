env["ir.attachment"].search(["&",["res_model", "=", "ir.ui.view"],"|",["name", "=like", "%.assets_%.css"],["name", "=like", "%.assets_%.js"],]).unlink()
env.cr.commit()