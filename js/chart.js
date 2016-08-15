
var owner = "bgabor666";
var repository = "csibe-results";
var branch = "master";

var arm_targets = [
    "clang-trunk-cortex-m0",
    "clang-trunk-cortex-m4"
];

var x86_targets = [
    "clang-trunk-x86_64"
];

var project_names = [
    "mpgcut-1.1",
    "jpeg-6b",
    "zlib-1.1.4",
    "replaypc-0.4.0.preproc",
    "OpenTCP-1.0.4",
    "bzip2-1.0.2",
    "mpeg2dec-0.3.1",
    "jikespg-1.3",
    "libmspack",
    "compiler",
    "teem-1.6.0-src",
    "ttt-0.10.1.preproc",
    "unrarlib-0.4.0",
    "libpng-1.2.5",
    "flex-2.5.31",
    "cg_compiler_opensrc",
    "lwip-0.5.3.preproc"
];

var chart_div = document.querySelector('#chart_div_cm');

var tree_url = "https://api.github.com/repos/"
                + owner + "/" + repository + "/git/trees/" + branch + "?recursive=1";

var repository_tree;

var raw_url_prefix = "https://raw.githubusercontent.com/"
                + owner + "/" + repository + "/" + branch + "/";

var all_results = [];
var all_results_initialized = false;

google.charts.load('current', { packages: ['corechart', 'line'] });

function findAlias(name) {
    switch (name) {
        case "clang-trunk-cortex-m0":
            return "Cortex-M0";
        case "clang-trunk-cortex-m4":
            return "Cortex-M4";
        case "clang-trunk-x86_64":
            return "x86-64";
        default:
            return name;
    }
}

function drawChart(columns, rows, title) {
    var data = new google.visualization.DataTable();

    for (var i = 0; i < columns.length; i++) {
        var column = columns[i];
        data.addColumn(column[1], findAlias(column[0]));
    }

    data.addRows(rows);

    var options = {
        title: title,
        curveType: 'function'
    };

    var chart = new google.visualization.LineChart(chart_div);
    chart.draw(data, options);
}

function csvToJSON(csv, url) {
    var data = {};
    var sum_all = 0;
    var lines = csv.split("\n");
    for (var i = 0; i < lines.length; i++) {
        if (lines[i].length == 0)
            continue;
        var currentline = lines[i].split(",");
        if (currentline.length == 3 && currentline[2] % 1 === 0 && currentline[2] > 0) {
            var project_name = currentline[0];
            var file_name = currentline[1];
            var size = parseInt(currentline[2]);
            sum_all += size;

            if (typeof(data[project_name]) === "undefined")
                data[project_name] = [];
            data[project_name].push([file_name, size]);
        } else if (currentline.length == 2)
            data[currentline[0]] = currentline[1];
    }

    // Extra properties
    data["sum"] = sum_all;

    var platform = url.split("/")[6];
    data["platform"] = platform;

    return data;
}

function getURL(url) {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onload = function() {
            var status = xhr.status;
            if (status == 200) {
                var response = {
                    url: xhr.responseURL,
                    content: xhr.response
                };
                resolve(response);
            } else {
                console.log("getURL() error, status: " + status);
                reject(status);
            }
        };
        xhr.send();
    });
};

function downloadRepositoryTree() {
    if (repository_tree === undefined) {
        return getURL(tree_url).then(function(response) {
            repository_tree = JSON.parse(response.content).tree;
        }, function(status) {
            console.log("Can't access repository tree.");
            return null;
        });
    } else
        return Promise.resolve();
}

function getFileList(targets) {
    return downloadRepositoryTree().then(function() {
        var file_list = [];
        for (var node of repository_tree) {
            var platform = node.path.split('/')[0];
            if (node.type == "blob" && node.path.endsWith(".csv") && targets.includes(platform))
                file_list.push(node.path);
        }
        return file_list;
    });
}

function downloadResultsInParallel(targets) {
    var results = [];
    return getFileList(targets).then(function(list) {
        for (var i = 0; i < list.length; i++) {
            list[i] = getURL(raw_url_prefix + list[i] + '?' + new Date().getTime()).then(function(response) {
                results.push(csvToJSON(response.content, response.url));
            });
        }
        return list;
    }).then(function(promise_list) {
        return Promise.all(promise_list).then(function() {
            return results;
        });
    });
}

function downloadAllResults() {
    if (all_results_initialized == false) {
        return downloadResultsInParallel(arm_targets).then(function(arm_results) {
            all_results = all_results.concat(arm_results);
            return downloadResultsInParallel(x86_targets).then(function(x86_results) {
                all_results = all_results.concat(x86_results);
                all_results_initialized = true;
            });
        });
    } else {
        return Promise.resolve();
    }
}

function getIndexByColumnName(columns, name) {
    for (var i = 0; i < columns.length; i++) {
        if (columns[i][0] == name)
            return i;
    }
}

function summarizePlatformResultsByProject(project_name) {
    var columns = [
        ["Date", "string"]
    ];
    var platform_names = arm_targets.concat(x86_targets);
    for (var i = 0; i < platform_names.length; i++)
        columns.push([platform_names[i], "number"]);

    var rows = [];

    return downloadAllResults().then(function() {
        for (var i = 0; i < all_results.length; i++) {
            var current_result = all_results[i];

            var sum = 0;
            if (project_name != "all") {
                var current_project = current_result[project_name];
                for (var k = 0; k < current_project.length; k++) {
                    var file = current_project[k];
                    sum += file[1];
                }
            } else
                sum = current_result["sum"];

            // Find or create a new row
            var current_row = -1;
            for (var j = 0; j < rows.length; j++) {
                if (rows[j][0] == current_result.Date) {
                    current_row = j;
                    break;
                }
            }
            if (current_row == -1)
                current_row = rows.push([current_result.Date]) - 1;

            // Find the column and insert
            for (var j = 1; j < columns.length; j++) {
                var column_name = columns[j][0];

                if (current_result["platform"] == column_name) {
                    var index = getIndexByColumnName(columns, column_name);
                    rows[current_row][index] = sum;
                    break;
                }
            }
        }

        // Sort rows by date
        rows.sort(function(a, b){
            return new Date(a[0]) - new Date(b[0]);
        });
    }).then(function() {
        var chart_data = {
            columns: columns,
            rows: rows
        };
        return chart_data;
    });
}

function filterByDate(rows, from) {
    var from_date = new Date(from);
    for (var i = 0; i < rows.length; i++) {
        var row_date = new Date(rows[i][0]);
        console.log(from_date + "<" + row_date);
        if (from_date > row_date) {
            rows.splice(i, 1);
            i--;
        }
    }
    return rows;
}

function showPlatforms(arch, project, from) {
    chart_div.innerHTML = "Collecting data...";

    summarizePlatformResultsByProject(project).then(function(chart_data) {
        // Filter by arch
        if (arch != "all") {
            for (var i = 1; i < chart_data.columns.length; i++) {
                if (arch != "arm" && arm_targets.includes(chart_data.columns[i][0])
                        || arch != "x86" && x86_targets.includes(chart_data.columns[i][0])) {
                    chart_data.columns.splice(i, 1);
                    for (var j = 0; j < chart_data.rows.length; j++) {
                        chart_data.rows[j].splice(i, 1);
                    }
                    i--;
                }
            }
        }

        // Filter by date
        chart_data.rows = filterByDate(chart_data.rows, from);

        var title = "CSiBE code size";
        if (project != "all")
            title += " of " + project;

        drawChart(chart_data.columns, chart_data.rows, title);
    });
}
