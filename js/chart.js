
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

var chart_filter = {
    arch : "all",
    project : "all",
    from_date : "2016-01-01"
};

var tree_url = "https://api.github.com/repos/"
                + owner + "/" + repository + "/git/trees/" + branch + "?recursive=1";

var repository_tree = [];

var raw_url_prefix = "https://raw.githubusercontent.com/"
                + owner + "/" + repository + "/" + branch + "/";

var csibe_results = [];

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
    if (repository_tree.length == 0) {
        return getURL(tree_url).then(function(response) {
            var tree = JSON.parse(response.content).tree;
            for (var node of tree) {
                if (node.type == "blob" && node.path.endsWith(".csv")) {
                    var node_path = node.path.split('/');
                    var csv_node = {
                        path : node.path,
                        platform : node_path[0],
                        date : new Date(node_path[3].substring(0, 10)),
                        downloaded: false
                    };
                    repository_tree.push(csv_node);
                }
            }
        }, function(status) {
            console.log("Can't access repository tree.");
            return null;
        });
    } else
        return Promise.resolve();
}

function getFilteredFileList() {
    return downloadRepositoryTree().then(function() {
        var file_list = [];
        var from_date = new Date(chart_filter.from_date);
        for (var node of repository_tree) {
            if ((chart_filter.arch == "all"
                || chart_filter.arch == "arm" && arm_targets.includes(node.platform)
                || chart_filter.arch == "x86" && x86_targets.includes(node.platform))
                && new Date(node.date) >= from_date)
                file_list.push(node);
        }
        return file_list;
    });
}

function downloadNecessaryResults() {
    var pending = [];
    var results = [];
    return getFilteredFileList().then(function(list) {
        for (var node of list) {
            if (!node.downloaded) {
                node.downloaded = true;
                pending.push(getURL(raw_url_prefix + node.path + '?' + new Date().getTime()).then(function(response) {
                    results.push(csvToJSON(response.content, response.url));
                }));
            }
        }
        return pending;
    }).then(function(pending_list) {
        return Promise.all(pending_list).then(function() {
            csibe_results = csibe_results.concat(results);
        });
    });
}

function summarizePlatformResultsByProject() {
    var columns = [
        ["Date", "string"]
    ];

    var arch = chart_filter.arch;
    if (arch == "all" || arch == "arm") {
        for (var platform of arm_targets)
            columns.push([platform, "number"]);
    }
    if (arch == "all" || arch == "x86") {
        for (var platform of x86_targets)
            columns.push([platform, "number"]);
    }

    var rows = [];

    return downloadNecessaryResults().then(function() {
        for (var current_result of csibe_results) {
            // Filter by date
            if (new Date(current_result.Date) < new Date(chart_filter.from_date))
                continue;

            // Summarize all projects or just the specified one
            var sum = 0;
            if (chart_filter.project != "all") {
                var current_project = current_result[chart_filter.project];
                for (var file of current_project)
                    sum += file[1];
            } else
                sum = current_result["sum"];

            // Find or create a new row
            var current_row = -1;
            for (var i = 0; i < rows.length; i++) {
                if (rows[i][0] == current_result.Date) {
                    current_row = i;
                    break;
                }
            }
            if (current_row == -1)
                current_row = rows.push([current_result.Date]) - 1;

            // Find the column and insert
            for (var i = 1; i < columns.length; i++) {
                var column_name = columns[i][0];
                if (current_result["platform"] == column_name) {
                    rows[current_row][i] = sum;
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

function showPlatforms() {
    chart_div.innerHTML = "Collecting data...";

    summarizePlatformResultsByProject().then(function(chart_data) {
        var title = "CSiBE code size";
        if (chart_filter.project != "all")
            title += " of " + chart_filter.project;

        drawChart(chart_data.columns, chart_data.rows, title);
    });
}
