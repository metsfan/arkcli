var OFFLINE = 0, STARTING = 1, ONLINE = 2;

$(document).ready(function() {
  $("#info").hide();
  $("#install").hide();
  $("#config").hide();

  $("#use_server_name").on("click", function() {
    pywebview.api.useName($("#server_name").val())
      .catch(onBackendError)
  });

  $("#reload_config").on("click", function() {
    pywebview.api.reload()
      .catch(onBackendError)
  }).hide();

  $("#start_button").on("click", function() {
    pywebview.api.start()
      .catch(onBackendError);
    $(this).prop('disabled', true);
  });

  $("#stop_button").on("click", function() {
    var useWarning = $("#stop_with_warning").is(":checked");
    var warningTime = parseInt($("#stop_warning").val());
    pywebview.api.stop(useWarning, warningTime)
      .catch(onBackendError);
  });

  $("#update_button").on("click", function() {
    var useWarning = $("#stop_with_warning").is(":checked");
    var warningTime = parseInt($("#stop_warning").val());
    pywebview.api.update(useWarning, warningTime)
      .catch(onBackendError);
  });

  $("#restart_button").on("click", function() {
    var useWarning = $("#stop_with_warning").is(":checked");
    var warningTime = parseInt($("#stop_warning").val());
    pywebview.api.restart(useWarning, warningTime)
      .catch(onBackendError);
  });

  $("#backup_select").on("focus", function() {
    pywebview.api.fetchBackups()
      .then(function(backups) {
        var backupSelectElem = $("#backup_select");
        backupSelectElem.empty()
          .append("<option>Select Backup...</option>");

        for (var i = 0; i < backups.length; i++) {
          backupSelectElem.append("<option value=\"" + backups[i] + "\">" + backups[i] + "</option>");
        }
      })
      .catch(onBackendError);
  });

  $("#restore_button").on("click", function() {
    var backup = $("#backup_select").val();
    if (backup) {
      pywebview.api.restore(backup)
        .catch(onBackendError);
    }
  });

  $("#cleanup_button").on("click", function() {
    pywebview.api.cleanup()
      .catch(onBackendError);
  });

  $("#backup_button").on("click", function() {
    pywebview.api.backup()
      .catch(onBackendError);
  });

  $("#stop_with_warning").on("change", function() {
    $("#stop_with_warning_control").toggle();
  });

  $("#install_button").on("click", function() {
    pywebview.api.install()
      .catch(onBackendError)
  });

  $("#execute_rcon_command").on("click", function() {
    pywebview.api.rconcmd($("#rcon_command").val())
      .catch(onBackendError)
  });

  $("#open_server_config").on("click", function() {
    pywebview.api.open_server_config()
      .catch(onBackendError);
  });
});

function sync(data) {
  $("#reload_config").show();
  $("#config").show();

  if (data.installed) {
    $("#install").hide();
    $("#info").show();
    $("#update_button").show();

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
    $("#update_button").hide();
    $("#install").show();

    if (data.installing) {
      $("#installing").show();
      $("#not_installed").hide();
      $("#install_button").prop("disabled", true);
    } else {
      $("#installing").hide();
      $("#not_installed").show();
      $("#install_button").prop("disabled", false);
    }
  }

  renderLog(data.log)
}

function renderLog(log) {
  var html = "";
  for (var i = log.length - 1; i >= 0; i--) {
    html += '<p class="level_' + log[i].level + '">' + log[i].data + '</p>'
  }

  $("#log").html(html);
}

function onBackendError(e) {
  console.log(e);
  alert(e.message);
}
