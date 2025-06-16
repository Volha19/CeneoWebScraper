
function contentFormatter(value, row) {
  return value ? value.substring(0, 100) + (value.length > 100 ? '...' : '') : '-';
}

function prosFormatter(value, row) {
  if (!value || value.length === 0) return '-';
  return '<ul>' + value.map(pro => pro ? `<li>${pro}</li>` : '').join('') + '</ul>';
}

function consFormatter(value, row) {
  if (!value || value.length === 0) return '-';
  return '<ul>' + value.map(con => con ? `<li>${con}</li>` : '').join('') + '</ul>';
}

$(function() {
  $('#reviewsTable').bootstrapTable({
    pagination: true,
    pageSize: 10,
    search: true,
    filterControl: true
  });
});

