var OFFLINE = 0, STARTING = 1, ONLINE = 2;

$(document).ready(function() {
  $("#info").hide();
  $("#install").hide();

  $("#use_server_name").on("click", function() {
    pywebview.api.useName($("#server_name").val())
  });

  $("#start_button").on("click", function() {
    pywebview.api.start();
    $(this).prop('disabled', true);
  });

  $("#stop_button").on("click", function() {
    var useWarning = $("#stop_with_warning").is(":checked");
    var warningTime = parseInt($("#stop_warning").val());
    pywebview.api.stop(useWarning, warningTime);
  });

  $("#restart_button").on("click", function() {
    var useWarning = $("#stop_with_warning").is(":checked");
    var warningTime = parseInt($("#stop_warning").val());
    pywebview.api.restart(useWarning, warningTime);
  });

  $("#backup_select").on("click", function() {
    var backups = pywebview.api.fetchBackups();

    var backupSelectElem = $("#backup_select");
    backupSelectElem.empty()
      .append("<option>Select Backup...</option>");

    for (var i = 0; i < backups.length; i++) {
      backupSelectElem.append("<option value=\"" + backups[i] + "\">" + backups[i] + "</option>");
    }
  });

  $("#restore_button").on("click", function() {
    var backup = $("#backup_select").val();
    if (backup) {
      pywebview.api.restoreFromBackup(backup);
    }
  });

  $("#cleanup_button").on("click", function() {
    pywebview.api.cleanup();
  });

  $("#backup_button").on("click", function() {
    pywebview.api.backup();
  });

  $("#stop_with_warning").on("change", function() {
    $("#stop_with_warning_control").toggle();
  });

  $("#install_button").on("click", function() {
    pywebview.api.install()
  })
});

function sync(data) {
  if (data.installed) {
    $("#info").show();
    $("#install").hide();

    var statusElem = $("#status");
    var startButtonElem = $("#start_button");
    var restartButtonElem = $("#restart_button");
    var stopButtonElem = $("#stop_button");
    var statsElem = $("#stats");

    switch (data.server_status) {
      case OFFLINE:
        statusElem.html("Offline");
        statusElem.attr("class", "offline");

        startButtonElem.prop('disabled', false);
        restartButtonElem.prop('disabled', true);
        stopButtonElem.prop('disabled', true);

        statsElem.hide();
        break;

      case STARTING:
        statusElem.html("Starting");
        statusElem.attr("class", "starting");

        startButtonElem.prop('disabled', true);
        restartButtonElem.prop('disabled', false);
        stopButtonElem.prop('disabled', false);

        statsElem.hide();
        break;

      case ONLINE:
        statusElem.html("Online (pid " + data.running_pid + ")");
        statusElem.attr("class", "starting");

        startButtonElem.prop('disabled', true);
        restartButtonElem.prop('disabled', false);
        stopButtonElem.prop('disabled', false);

        statsElem.show();

        $("#players_online").html(data.server_info.player_count + "/" + data.server_info.max_players);
        $("#server_label").html(data.server_info.server_name);
        $("#map_label").html(data.server_info.map);
        break;
    }
  } else {
    $("#info").hide();
    $("#install").show();

    if (data.installing) {
      $("#installing").show();
      $("#not_installed").hide();
      $("#install_button").prop("disable", true)
    } else {
      $("#installing").hide();
      $("#not_installed").show();
      $("#install_button").prop("disable", false)
    }
  }
}
