$('#BugReportModal').on('shown.bs.modal', function () {
    update_url('search');
    $(".share-link").val(location.href);
    $(".share-link").focus();
    $(".share-link").select();
});
