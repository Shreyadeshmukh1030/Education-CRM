import os

base_dir = "C:/Users/HP/Desktop/Education-CRM/templates/timetable"
os.makedirs(base_dir, exist_ok=True)

models = {
    'period': {'title': 'Periods', 'fields': ['name', 'start_time', 'end_time', 'is_break', 'order'], 'obj': 'period_obj'},
    'schedule': {'title': 'Class Schedules', 'fields': ['class_assigned', 'period', 'day_of_week', 'subject', 'teacher', 'room'], 'obj': 'schedule_obj'},
}

list_template = """{{% extends 'base/base.html' %}}

{{% block title %}}{title} - EduCore CRM{{% endblock %}}

{{% block content %}}
<div class="dashboard-header animate-fade-in stagger-1" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
    <div>
        <h1 style="font-size: 2rem; margin-bottom: 5px;">{title}</h1>
        <p style="color: var(--text-muted);">Manage {title_lower}.</p>
    </div>
    <a href="{{% url '{model}_add' %}}" class="btn btn-primary" style="background-color: var(--primary-color); color: #fff; box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);">
        <i class="ph ph-plus-circle" style="margin-right: 8px; font-size: 1.2rem;"></i> Add {model_cap}
    </a>
</div>

<div class="card animate-fade-in stagger-2" style="padding: 0; overflow: hidden;">
    <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead style="background-color: var(--background-color); border-bottom: 2px solid var(--border-color);">
                <tr>
                    {headers}
                    <th style="padding: 15px 20px; font-weight: 600; color: var(--text-muted); text-align: right;">Actions</th>
                </tr>
            </thead>
            <tbody>
                {{% for {obj} in {model}s %}}
                <tr style="border-bottom: 1px solid var(--border-color); transition: background-color var(--transition-fast);">
                    {cells}
                    <td style="padding: 15px 20px; text-align: right;">
                        <a href="{{% url '{model}_edit' {obj}.pk %}}" style="color: var(--text-muted); margin-right: 10px; transition: color var(--transition-fast);" onmouseover="this.style.color='var(--primary-color)'" onmouseout="this.style.color='var(--text-muted)'"><i class="ph ph-pencil-simple" style="font-size: 1.2rem;"></i></a>
                        <a href="{{% url '{model}_delete' {obj}.pk %}}" style="color: var(--text-muted); transition: color var(--transition-fast);" onmouseover="this.style.color='var(--danger-color)'" onmouseout="this.style.color='var(--text-muted)'"><i class="ph ph-trash" style="font-size: 1.2rem;"></i></a>
                    </td>
                </tr>
                {{% empty %}}
                <tr>
                    <td colspan="100" style="padding: 30px; text-align: center; color: var(--text-muted);">
                        <p>No {title_lower} found.</p>
                    </td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>
    </div>
</div>
{{% endblock %}}
"""

form_template = """{{% extends 'base/base.html' %}}

{{% block title %}}Add/Edit {model_cap} - EduCore CRM{{% endblock %}}

{{% block content %}}
<div class="dashboard-header animate-fade-in stagger-1" style="margin-bottom: 24px;">
    <a href="{{% url '{model}_list' %}}" style="color: var(--text-muted); text-decoration: none; display: inline-flex; align-items: center; margin-bottom: 10px;">
        <i class="ph ph-arrow-left" style="margin-right: 5px;"></i> Back to {title}
    </a>
    <h1 style="font-size: 2rem; margin-bottom: 5px;">{{% if object %}}Edit{{% else %}}Add{{% endif %}} {model_cap}</h1>
</div>

<div class="card animate-fade-in stagger-2" style="max-width: 600px;">
    <form method="post" enctype="multipart/form-data">
        {{% csrf_token %}}
        {{% for field in form %}}
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-weight: 500;">{{{{ field.label }}}}</label>
                {{{{ field }}}}
                {{% if field.errors %}}
                    <div style="color: var(--danger-color); font-size: 0.85rem; margin-top: 5px;">{{{{ field.errors }}}}</div>
                {{% endif %}}
                {{% if field.help_text %}}
                    <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 5px;">{{{{ field.help_text }}}}</div>
                {{% endif %}}
            </div>
        {{% endfor %}}
        
        <div style="margin-top: 24px; display: flex; gap: 10px;">
            <button type="submit" class="btn btn-primary" style="background-color: var(--primary-color); color: #fff;">Save {model_cap}</button>
            <a href="{{% url '{model}_list' %}}" class="btn" style="background-color: var(--background-color); color: var(--text-color); border: 1px solid var(--border-color);">Cancel</a>
        </div>
    </form>
</div>

<style>
    form input[type="text"], form input[type="number"], form input[type="email"], form input[type="date"], form input[type="time"], form select, form textarea {{
        width: 100%;
        padding: 10px 15px;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        background-color: var(--background-color);
        color: var(--text-color);
    }}
</style>
{{% endblock %}}
"""

delete_template = """{{% extends 'base/base.html' %}}

{{% block title %}}Delete {model_cap} - EduCore CRM{{% endblock %}}

{{% block content %}}
<div class="dashboard-header animate-fade-in stagger-1" style="margin-bottom: 24px;">
    <h1 style="font-size: 2rem; margin-bottom: 5px;">Delete {model_cap}</h1>
</div>

<div class="card animate-fade-in stagger-2" style="max-width: 600px; border-left: 4px solid var(--danger-color);">
    <p>Are you sure you want to delete the {model_cap} <strong>"{{{{ object }}}}"</strong>?</p>
    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px;">This action cannot be undone.</p>
    
    <form method="post">
        {{% csrf_token %}}
        <div style="display: flex; gap: 10px;">
            <button type="submit" class="btn btn-primary" style="background-color: var(--danger-color); color: #fff;">Yes, Delete</button>
            <a href="{{% url '{model}_list' %}}" class="btn" style="background-color: var(--background-color); color: var(--text-color); border: 1px solid var(--border-color);">Cancel</a>
        </div>
    </form>
</div>
{{% endblock %}}
"""

for model, data in models.items():
    headers = "\n".join([f'<th style="padding: 15px 20px; font-weight: 600; color: var(--text-muted);">{f.replace("_", " ").title()}</th>' for f in data['fields']])
    cells = "\n".join([f'<td style="padding: 15px 20px; color: var(--text-muted);">{{{{ {data["obj"]}.{f} }}}}</td>' for f in data['fields']])
    
    # List
    with open(os.path.join(base_dir, f"{model}_list.html"), "w") as f:
        f.write(list_template.format(
            title=data['title'], title_lower=data['title'].lower(), model=model, model_cap=model.capitalize(),
            headers=headers, cells=cells, obj=data['obj']
        ).replace("{{%", "{%").replace("%}}", "%}"))
        
    # Form
    with open(os.path.join(base_dir, f"{model}_form.html"), "w") as f:
        f.write(form_template.format(
            title=data['title'], model=model, model_cap=model.capitalize()
        ).replace("{{%", "{%").replace("%}}", "%}"))
        
    # Delete
    with open(os.path.join(base_dir, f"{model}_confirm_delete.html"), "w") as f:
        f.write(delete_template.format(
            model=model, model_cap=model.capitalize()
        ).replace("{{%", "{%").replace("%}}", "%}"))

print("Timetable templates generated successfully!")
