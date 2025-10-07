frappe.pages['library_dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Library Dashboard',
		single_column: true
	});
  // Fetch data from your API
  frappe.call({
    method: "library_management.api.get_library_stats",
    callback: function(r) {
      if (r.message) {
        render_dashboard(r.message);
      }
    }
  });

  function render_dashboard(data) {
    const html = `
      <div class="row" style="margin-top:20px;">
        <div class="col-sm-4">
          <div class="card">
            <div class="card-body">
              <h5 style="color:black;">Total Books</h5>
              <h2 style="color:black;">${data.books}</h2>
            </div>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="card">
            <div class="card-body">
              <h5 style="color:black;">Total Members</h5>
              <h2 style="color:black;">${data.members}</h2>
            </div>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="card">
            <div class="card-body">
              <h5 style="color:black;">Issued Books</h5>
              <h2 style="color:black;">${data.issued}</h2>
            </div>
          </div>
        </div>
      </div>
    `;
    $(wrapper).find('.page-content').html(html);
  }
};