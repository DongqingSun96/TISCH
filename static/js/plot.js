//     Plotly.d3.csv("/static/image/tSNE/AML_GSE116256_AML_umap.csv", function(err, rows) {

//         function unpack(rows, key) {
//             return rows.map(function(row) { return row[key]; });
//         }

//         var data = [{
//             type: 'scatter',
//             x: unpack(rows, 'UMAP_1'),
//             y: unpack(rows, 'UMAP_2'),
//             mode: 'markers',
//             transforms: [{
//                 type: 'groupby',
//                 groups: unpack(rows, 'assign.ident'),
//             }],
//             marker: { size: 2 }, 
//             hovertext: unpack(rows, 'Cell'),
//             hoverinfo: 'all'
//         }]

//         var layout = {
//             autosize: true,
//             title: "AML_GSE116256_AML",
//             legend: {
//                 traceorder: 'normal',
//             },
//             yaxis: {
//                 scaleanchor: "x",
//             },
//         }

//         var config = {
//             toImageButtonOptions: {
//                 format: 'png', // one of png, svg, jpeg, webp
//                 filename: 'custom_image',
//                 height: 750,
//                 width: 1050,
//                 scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
//             }
//         }

//         Plotly.newPlot('overview', data, layout, config);
//     });

// var data=Plotly.d3.json("/static/image/tSNE/AML_GSE116256_AML_umap.json")

var DefaulfColorPalette = [
    "#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
    "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
    "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
    "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
    "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D"
];
var DefaultColorBorder = "#595959"

function FindallIndex(a, x) {
    var all_index = [];
    var i = 0;
    while (i < a.length) {
        i = a.indexOf(x, i);
        if (i == -1) {
            break;
        }
        all_index.push(i);
        i = i + 1;
    }
    return all_index;
}

function PlotUMAP(data_file, title_name, plot_id) {
    Plotly.d3.json(data_file, function(error, data_use) {
        var marker_size;
        console.log(data_use);
        if (data_use.UMAP_1.length > 15000) {
            marker_size = 2
        } else {
            marker_size = 3
        }
        console.log(marker_size);
        var data = [{
            type: 'scatter',
            x: data_use.UMAP_1,
            y: data_use.UMAP_2,
            mode: 'markers',
            transforms: [{
                type: 'groupby',
                groups: data_use.Celltype_curated
            }],
            marker: {
                size: marker_size
            },
            text: data_use.Cell,
            hovertemplate: "%{text}<br><b>%{fullData.name}</b><extra></extra>",
            hoverinfo: 'text'
        }];

        var layout = {
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
                itemsizing: 'constant'
            },
            xaxis: {
                autorange: true
            },
            yaxis: {
                scaleanchor: 'x',
                autorange: true
            },
            colorway: DefaulfColorPalette,
            margin: {
                l: 40
            }
        };

        var filename = title_name + "_umap";
        var config = {
            hovermode: 'closest',
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: filename,
                height: 750,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.react(plot_id, data, layout, config);
    });
};



function PlotUMAPMultiple(data_file, title_name, plot_id, annotation, selected_base, selected_cluster) {
    Plotly.d3.json(data_file, function(error, data_use) {

        // var data_use = data_use, selected_base = selected_base;
        // console.log(selected_base);
        var selected_data = {};
        if (selected_cluster == "All cells") {
            selected_data = data_use;
        } else {
            var selected_index = FindallIndex(data_use[selected_base], selected_cluster);
            // console.log(selected_index);

            for (key in data_use) {
                var selected = selected_index.map(function(i) {
                    return data_use[key][i]
                });
                selected_data[key] = selected;
            }
        }

        var marker_size;
        if (selected_data.UMAP_1.length > 15000) {
            marker_size = 2
        } else {
            marker_size = 3
        }
        var data = [{
            type: 'scatter',
            x: selected_data.UMAP_1,
            y: selected_data.UMAP_2,
            mode: 'markers',
            transforms: [{
                type: 'groupby',
                groups: selected_data[annotation]
            }],
            marker: {
                size: marker_size
            },
            text: selected_data.Cell,
            hovertemplate: "%{text}<br><b>%{fullData.name}</b><extra></extra>",
            hoverinfo: 'text'
        }];

        var layout = {
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
                itemsizing: 'constant'
            },
            xaxis: {
                autorange: true
            },
            yaxis: {
                scaleanchor: 'x',
                autorange: true
            },
            colorway: DefaulfColorPalette,
            margin: {
                l: 40
            }
        };

        var filename = title_name + "_umap";
        var config = {
            hovermode: 'closest',
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: filename,
                height: 750,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.newPlot(plot_id, data, layout, config);
    });
};

// Plotly.d3.json("/static/image/tSNE/AML_GSE116256_AML_umap_plot.json", function(error, figure) {
//     var data = [figure[0]]
//     var layout = figure[1]

//     var config = {
//         toImageButtonOptions: {
//             format: 'png', // one of png, svg, jpeg, webp
//             filename: 'custom_image',
//             height: 750,
//             width: 1050,
//             scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
//         }
//     }

//     Plotly.newPlot('overview', data, layout, config);
// });

// function PlotViolin(data_file, title_name) {
//     Plotly.d3.json(data_file, function(error, data_use) {

//         function TransformStyle(ident) {
//             var ident_new = ident.concat([]);
//             var unique_ident = jQuery.uniqueSort(ident_new);
//             var transform_style = new Array();
//             for (var i = 0; i < unique_ident.length; i++) {
//                 var style_target = {
//                     target: unique_ident[i],
//                     value: {
//                         fillcolor: DefaulfColorPalette[i % DefaulfColorPalette.length]
//                     }
//                 };
//                 transform_style.push(style_target);
//             };
//             return transform_style;
//         }


//         var data = [{
//             type: 'violin',
//             x: data_use.assign_CIBERSORT,
//             y: data_use.expression,
//             line: {
//                 width: 1,
//                 color: DefaultColorBorder,
//             },
//             transforms: [{
//                 type: 'groupby',
//                 groups: data_use.assign_CIBERSORT,
//                 styles: TransformStyle(data_use.assign_CIBERSORT)
//             }],
//             spanmode: 'hard',
//             scalemode: 'width',
//             box: {
//                 visible: true,
//                 width: 0.05
//             },
//             points: false
//         }];
//         console.log(data);

//         var layout = {
//             autosize: true,
//             title: title_name,
//             legend: {
//                 traceorder: 'normal',
//             },
//             // colorway: DefaulfColorPalette
//         };

//         var config = {
//             toImageButtonOptions: {
//                 format: 'png', // one of png, svg, jpeg, webp
//                 filename: 'custom_image',
//                 height: 400,
//                 width: 1050,
//                 scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
//             }
//         };

//         Plotly.newPlot('gene', data, layout, config);
//     });
// };

function PlotViolin(data_file, title_name) {
    Plotly.d3.json(data_file, function(error, data_use) {
        function FormData() {
            var data_array = new Array();
            var idx = 0;
            for (ident in data_use) {
                var trace = {
                    type: 'violin',
                    name: ident,
                    y: data_use[ident],
                    line: {
                        width: 1,
                        color: DefaultColorBorder,
                    },
                    fillcolor: DefaulfColorPalette[idx % DefaulfColorPalette.length],
                    spanmode: 'hard',
                    scalemode: 'width',
                    box: {
                        visible: true,
                        width: 0.05
                    },
                    points: false,
                    meanline: {
                        visible: true
                    },
                    hoveron: 'violins+kde'
                };
                data_array.push(trace);
                idx++;
            };
            return data_array
        }
        var data = FormData();

        var layout = {
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
            },
            margin: {
                l: 40
            }
            // colorway: DefaulfColorPalette
        };

        var config = {
            responsive: true,
            toImageButtonOptions: {
                format: 'svg', // one of png, svg, jpeg, webp
                filename: 'custom_image',
                height: 400,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.react('gene-violin', data, layout, config);
    });
};

function PlotViolinMultiple(data_file, title_name, comparison, group) {
    Plotly.d3.json(data_file, function(error, data_use) {
        if (group == "None") {
            group = comparison;
            var violin_mode = "overlay";
        } else {
            var violin_mode = "group";
        }

        function FormData() {
            if (group == "None") {
                group = comparison
            }
            var ident_new1 = data_use[group].concat([]).sort();
            var unique_ident1 = jQuery.uniqueSort(ident_new1);

            var data_array = new Array();
            for (var i = 0; i < unique_ident1.length; i++) {
                ident_index1 = FindallIndex(data_use[group], unique_ident1[i]);
                var selected_data = {};
                for (key in data_use) {
                    var selected = ident_index1.map(function(i) {
                        return data_use[key][i]
                    });
                    selected_data[key] = selected;
                }
                // var ident_new2 = selected_data[comparison].concat([]).sort();
                // var unique_ident2 = jQuery.uniqueSort(ident_new2);
                // for (var j = 0; j < unique_ident2.length; j++) {
                //     ident_index2 = FindallIndex(selected_data[comparison], unique_ident2[j]);
                //     var selected_data2 = {};
                //     for (key in selected_data) {
                //         var selected = ident_index2.map(function(i) {
                //             return selected_data[key][i]
                //         });
                //         selected_data2[key] = selected;
                //     }
                var trace = {
                    type: 'violin',
                    name: unique_ident1[i],
                    y: selected_data["expression"],
                    x: selected_data[comparison],
                    legendgroup: unique_ident1[i],
                    scalegroup: unique_ident1[i],
                    line: {
                        width: 1,
                        color: DefaultColorBorder,
                    },
                    fillcolor: DefaulfColorPalette[i % DefaulfColorPalette.length],
                    // transforms: [{
                    //     type: 'groupby',
                    //     groups: selected_data[comparison],
                    //     // styles: TransformStyle(data_use.assign_CIBERSORT)
                    // }],
                    spanmode: 'hard',
                    scalemode: 'width',
                    box: {
                        visible: true,
                        width: 0.05
                    },
                    points: false,
                    meanline: {
                        visible: true
                    },
                    hoveron: 'violins+kde'
                };
                data_array.push(trace);
            };
            return data_array;
        }

        var data = FormData();
        console.log(data);

        // var data = [{
        //     type: 'violin',
        //     x: data_use.patient,
        //     y: data_use.expression,
        //     line: {
        //         width: 1,
        //         color: DefaultColorBorder,
        //     },
        //     transforms: [{
        //         type: 'groupby',
        //         groups: data_use.patient,
        //         // styles: TransformStyle(data_use.patient)
        //     }],
        //     spanmode: 'hard',
        //     scalemode: 'width',
        //     box: {
        //         visible: true,
        //         width: 0.05
        //     },
        //     points: false
        // }];

        var layout = {
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
            },
            violinmode: violin_mode,
            margin: {
                l: 40
            }
            // colorway: DefaulfColorPalette
        };

        var config = {
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: 'custom_image',
                height: 400,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.newPlot('gene-violin', data, layout, config);
    });
};

function PlotBoxMultiple(data_file, title_name, comparison, group) {
    Plotly.d3.json(data_file, function(error, data_use) {
        if (group == "None") {
            group = comparison;
            var box_mode = "overlay";
        } else {
            var box_mode = "group";
        }

        function FormData() {
            var ident_new1 = data_use[group].concat([]).sort();
            var unique_ident1 = jQuery.uniqueSort(ident_new1);
            console.log(unique_ident1);
            var data_array = new Array();
            for (var i = 0; i < unique_ident1.length; i++) {
                ident_index1 = FindallIndex(data_use[group], unique_ident1[i]);
                var selected_data = {};
                for (key in data_use) {
                    var selected = ident_index1.map(function(i) {
                        return data_use[key][i]
                    });
                    selected_data[key] = selected;
                }
                // var ident_new2 = selected_data[comparison].concat([]).sort();
                // var unique_ident2 = jQuery.uniqueSort(ident_new2);
                // for (var j = 0; j < unique_ident2.length; j++) {
                //     ident_index2 = FindallIndex(selected_data[comparison], unique_ident2[j]);
                //     var selected_data2 = {};
                //     for (key in selected_data) {
                //         var selected = ident_index2.map(function(i) {
                //             return selected_data[key][i]
                //         });
                //         selected_data2[key] = selected;
                //     }
                var trace = {
                    type: 'box',
                    name: unique_ident1[i],
                    y: selected_data["expression"],
                    x: selected_data[comparison],
                    // legendgroup: unique_ident1[i],
                    // scalegroup: "All",
                    line: {
                        width: 1,
                        color: DefaultColorBorder,
                    },
                    fillcolor: DefaulfColorPalette[i % DefaulfColorPalette.length],
                    // transforms: [{
                    //     type: 'groupby',
                    //     groups: selected_data[comparison],
                    //     // styles: TransformStyle(data_use.assign_CIBERSORT)
                    // }],
                    // spanmode: 'hard',
                    // scalemode: 'width',
                    // box: {
                    //     visible: false,
                    //     width: 0.05
                    // },
                    points: false,
                    meanline: {
                        visible: true
                    },
                    // hoveron: 'violins+kde'
                };
                data_array.push(trace);
            };
            return data_array;
        }

        var data = FormData();
        console.log(data);

        // var data = [{
        //     type: 'violin',
        //     x: data_use.patient,
        //     y: data_use.expression,
        //     line: {
        //         width: 1,
        //         color: DefaultColorBorder,
        //     },
        //     transforms: [{
        //         type: 'groupby',
        //         groups: data_use.patient,
        //         // styles: TransformStyle(data_use.patient)
        //     }],
        //     spanmode: 'hard',
        //     scalemode: 'width',
        //     box: {
        //         visible: true,
        //         width: 0.05
        //     },
        //     points: false
        // }];

        var layout = {
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
            },
            boxmode: box_mode,
            margin: {
                l: 40
            }
            // colorway: DefaulfColorPalette
        };

        var config = {
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: 'custom_image',
                height: 400,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.newPlot('gene-violin', data, layout, config);
    });
};


function PlotUMAPGene(data_file, title_name, plot_id, label_name) {
    Plotly.d3.json(data_file, function(error, data_use) {
        var marker_size;
        if (data_use.UMAP_1.length > 15000) {
            marker_size = 2
        } else {
            marker_size = 3
        }
        var data = [{
            type: 'scatter',
            x: data_use.UMAP_1,
            y: data_use.UMAP_2,
            mode: 'markers',
            marker: {
                size: marker_size,
                color: data_use.expression,
                showscale: true,
                colorbar: {
                    title: {
                        text: "Expression"
                    }
                }
            },
            text: data_use.Cell,
            hovertemplate: "%{text}<br><b>" + label_name + ": %{marker.color:.2f}</b><extra></extra>",
            hoverinfo: 'text'
        }];

        var layout = {
            hovermode: 'closest',
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
                itemsizing: 'constant'
            },
            xaxis: {
                autorange: true
            },
            yaxis: {
                scaleanchor: 'x',
                autorange: true
            },
            margin: {
                l: 40
            }
            // colorway: DefaulfColorPalette
        };

        var config = {
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: 'custom_image',
                height: 750,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.react(plot_id, data, layout, config);
    });
};

function PlotUMAPGeneMultiple(data_file, title_name, plot_id, label_name, selected_base, selected_cluster) {
    Plotly.d3.json(data_file, function(error, data_use) {

        var selected_data = {};
        if (selected_cluster == "All cells") {
            selected_data = data_use;
        } else {
            var selected_index = FindallIndex(data_use[selected_base], selected_cluster);
            // console.log(selected_index);

            for (key in data_use) {
                var selected = selected_index.map(function(i) {
                    return data_use[key][i]
                });
                selected_data[key] = selected;
            }
        }

        var marker_size;
        if (selected_data.UMAP_1.length > 15000) {
            marker_size = 2
        } else {
            marker_size = 3
        }
        var data = [{
            type: 'scatter',
            x: selected_data.UMAP_1,
            y: selected_data.UMAP_2,
            mode: 'markers',
            marker: {
                size: marker_size,
                color: selected_data.expression,
                showscale: true,
                colorbar: {
                    title: {
                        text: "Expression"
                    }
                }
            },
            text: selected_data.Cell,
            hovertemplate: "%{text}<br><b>" + label_name + ": %{marker.color:.2f}</b><extra></extra>",
            hoverinfo: 'text'
        }];

        var layout = {
            hovermode: 'closest',
            autosize: true,
            title: title_name,
            legend: {
                traceorder: 'normal',
                itemsizing: 'constant'
            },
            xaxis: {
                autorange: true
            },
            yaxis: {
                scaleanchor: 'x',
                autorange: true
            },
            margin: {
                l: 40
            }
            // colorway: DefaulfColorPalette
        };

        var config = {
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: 'custom_image',
                height: 750,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.react(plot_id, data, layout, config);
    });
};


// Plotly.d3.json("/static/image/tSNE/AML_GSE116256_AML_ACP1_violin.json", function(error, figure) {
//     var data = [figure[0]]
//     var layout = figure[1]

//     var config = {
//         toImageButtonOptions: {
//             format: 'png', // one of png, svg, jpeg, webp
//             filename: 'custom_image',
//             height: 300,
//             width: 1050,
//             scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
//         }
//     }

//     Plotly.newPlot('gene', data, layout);
// });

function PlotDot(data_file, title_name, plot_id) {
    Plotly.d3.json(data_file, function(error, data_use) {
        var sizemin, sizemax;
        sizemin = Math.min.apply(null, data_use.percent);
        sizemax = Math.max.apply(null, data_use.percent);
        var size_number, plot_height;
        if (data_use.genenumber <= 5) {
            size_number = 3;
            plot_height = 350;
        } else if (data_use.genenumber <= 20) {
            size_number = 4;
            plot_height = 30 * data_use.genenumber + 200;
        } else if (data_use.genenumber > 20 & data_use.genenumber <= 50) {
            size_number = 5;
            plot_height = 30 * data_use.genenumber + 200;
        } else {
            size_number = 6;
            plot_height = 30 * data_use.genenumber + 200;
        }
        var size_x = [],
            size_y = [],
            size_array = [],
            size_text = [];

        var interval = (sizemax - sizemin) / (size_number - 1);
        size_x.push(0);
        size_y.push(0);
        size_array.push(sizemin);
        size_text.push(Math.round(sizemin) + "%");

        for (var i = 1; i < size_number; i++) {
            size_append = sizemin + i * interval;
            size_array.push(size_append);
            size_text.push(Math.round(size_append) + "%");
            size_x.push(0);
            size_y.push(i);
        }

        var data = [{
            type: 'scatter',
            x: data_use.celltype,
            y: data_use.gene,
            mode: 'markers',
            marker: {
                size: data_use.percent,
                sizemode: "diameter",
                sizeref: 3.5,
                sizemin: 2,
                color: data_use.expression,
                // colorscale: "RdBu",
                showscale: true,
                colorbar: {
                    title: {
                        text: "Average expression"
                    },
                    len: 0.5,
                    yanchor: "bottom",
                    x: 0.88,
                    xpad: 0
                }
            },
            hovertemplate: "<b>%{y}</b> in <b>%{x}</b><br>" +
                "<b>Expression: </b>%{marker.color: .2f}<br>" +
                "<b>Percent: </b>%{marker.size: .2f}%<extra></extra>",
            hoverinfo: 'text',
            showlegend: false,
        }];

        var dotsize = {
            type: 'scatter',
            x: size_x,
            y: size_y,
            xaxis: 'x2',
            yaxis: 'y2',
            mode: 'markers',
            marker: {
                size: size_array,
                sizemode: "diameter",
                sizeref: 3.5,
                sizemin: 2,
                color: "black"
            },
            hoverinfo: 'none',
            showlegend: false,
        };
        data.push(dotsize);

        var layout = {
            hovermode: 'closest',
            autosize: true,
            height: plot_height,
            title: title_name,
            legend: {
                traceorder: 'normal',
                itemsizing: 'constant'
            },
            xaxis: {
                automargin: true,
                domain: [0.05, 0.85]
            },
            xaxis2: {
                range: [-0.2, 0.6],
                domain: [0.865, 1],
                showgrid: false,
                showline: false,
                zeroline: false,
                showticklabels: false,
                // mirror: "all"
            },
            yaxis: {
                automargin: true
            },
            yaxis2: {
                anchor: 'x2',
                domain: [0.03, 0.48],
                showgrid: false,
                showline: false,
                zeroline: false,
                showticklabels: false,
                // mirror: true
            },
            annotations: [{
                text: "Percent expressed",
                showarrow: false,
                xanchor: 'left',
                x: 0.88,
                y: 0.49,
                xshift: -2.5,
                xref: 'paper',
                yref: 'paper',
            }],
            margin: {
                l: 40
            }
            // colorway: DefaulfColorPalette
        };

        for (var i = 0; i < size_array.length; i++) {
            sizetext = {
                text: size_text[i],
                showarrow: false,
                xanchor: 'left',
                x: 0.15,
                y: size_y[i],
                xref: 'x2',
                yref: 'y2',
            };
            layout.annotations.push(sizetext);
        }
        var config = {
            responsive: true,
            toImageButtonOptions: {
                format: 'png', // one of png, svg, jpeg, webp
                filename: 'custom_image',
                height: 750,
                width: 1050,
                scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
            }
        };

        Plotly.react(plot_id, data, layout, config);
    });
};

function PlotHeatmap(data_file, plot_id) {
    $.getJSON(data_file, function(data) {
        var data_expr = data.expression
        var cell_type = data.celltype
        var dataset = data.dataset
        var gene = data.gene
        // console.log(data_expr)
        // console.log(cell_type)
        // console.log(dataset)
        // console.log(gene)

        var layout_height = 30 * (dataset.length) + 250;
        if (layout_height < 400) {
            layout_height = 400;
        }

        var yvalue = [];
        for (var i = 0; i < dataset.length; i++) {
            yvalue.push("<a href='/data/" + dataset[i] + "' style='color: #54aced'>" + dataset[i] + "</a>")
        }

        function getPointCategoryName(point, dimension) {
            var series = point.series,
                isY = dimension === 'y',
                axis = series[isY ? 'yAxis' : 'xAxis'];
            return axis.categories[point[isY ? 'y' : 'x']];
        }

        Highcharts.chart(plot_id, {
            chart: {
                type: 'heatmap',
                marginTop: 50,
                marginBottom: 100,
                plotBorderWidth: 1,
                height: layout_height
            },

            title: {
                text: gene,
            },

            xAxis: {
                categories: cell_type,
                labels: {
                    style:{
                        color: 'black',
                        fontFamily: 'Arial',
                        fontSize: 12
                    }
                },
            },

            yAxis: {
                categories: yvalue,
                title: null,
                reversed: false,
                labels: {
                    style:{
                        fontFamily: 'Arial',
                        fontSize: 12
                    }
                }
            },

            accessibility: {
                point: {
                    descriptionFormatter: function (point) {
                        var ix = point.index + 1,
                            xName = getPointCategoryName(point, 'x'),
                            yName = getPointCategoryName(point, 'y'),
                            val = point.value;
                        return ix + '. ' + xName + ' in ' + yName + ', ' + val + '.';
                    }
                }
            },

            colorAxis: {
                min: 0,
                minColor: "#F0F0F0",
                // '#FFFFFF',
                maxColor:  "#A50F15",
                reversed: false,
            },

            legend: {
                align: 'right',
                layout: 'vertical',
                margin: 0,
                verticalAlign: 'top',
                y: 25,
                // symbolHeight: 280
            },

            tooltip: {
                formatter: function () {
                    return '<b> Dataset: ' + getPointCategoryName(this.point, 'y') + 
                    '</b> <br><b>Cell-type: ' + getPointCategoryName(this.point, 'x') + 
                    '</b> <br><b>Expression: ' + this.point.value + '</b>';
                }
            },

            series: [{
                turboThreshold: 0,
                name: 'Sales per employee',
                borderWidth: 0.2,
                borderColor: "#AFABAB" ,
                nullColor: "white",
                data: data_expr,
                dataLabels: {
                    enabled: true,
                    color: 'black',
                    style:{
                        fontSize: 10,
                        fontFamily: 'Arial',
                        fontWeight: 'normal',
                        // color: 'black',
                        textOutline: false
                    }
                }
            }],

            credits: false,

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500,
                    },
                    chartOptions: {
                        chart: {
                            className: 'small-chart'
                        }
                    }
                }]
            },

            exporting: {
                filename: "TISCH_" + gene + "_heatmap",
                sourceWidth: 1050,
                sourceHeight: layout_height,
                buttons: {
                    contextButton: {
                        menuItems: ["viewFullscreen", "separator", "downloadPNG", "downloadJPEG", "downloadPDF", "downloadSVG", "separator", "downloadCSV"]
                    }
                }

            }
        })

    })    
};


// function PlotHeatmap(data_file, title_name, plot_id) {
//     Plotly.d3.json(data_file, function(error, data_use) {
//         var zmin, zmax;
//         var expr_array = data_use.expression.join(",").split(",")
//         zmin = Math.min.apply(null, expr_array);
//         zmax = Math.max.apply(null, expr_array);

//         var dataset_text = [];
//         for (var i = 0; i < data_use.dataset.length; i++) {
//             var dataset = [];
//             for (var j = 0; j < data_use.celltype.length; j++) {
//                 dataset.push(data_use.dataset[i])
//             }
//             dataset_text.push(dataset);
//         }
//         var layout_height = 32 * (data_use.dataset.length) + 250;
//         if (layout_height < 400) {
//             layout_height = 400;
//         }


//         var yvalue = [];
//         for (var i = 0; i < data_use.dataset.length; i++) {
//             yvalue.push("<a href='/data/" + data_use.dataset[i] + "' style='color: #54aced'>" + data_use.dataset[i] + "</a>")
//         }

//         var data = [{
//             type: 'heatmap',
//             y: yvalue,
//             x: data_use.celltype,
//             z: data_use.expression,
//             mode: 'lines',
//             // colorscale: 'RdBu',
//             // colorscale: [
//             //     ['0.0', 'rgb(33,102,172)'],
//             //     ['0.125', 'rgb(67,147,195)'],
//             //     ['0.25', 'rgb(146,197,222)'],
//             //     ['0.375', 'rgb(209,229,240)'],
//             //     ['0.5', 'rgb(247,247,247)'],
//             //     ['0.625', 'rgb(253,219,199)'],
//             //     ['0.75', 'rgb(244,165,130)'],
//             //     ['0.875', 'rgb(214,96,77)'],
//             //     ['1.0', 'rgb(178,24,43)']
//             // ],
//             colorscale: "Reds",
//             // colorscale: [
//             //     ['0.0', 'rgb(5,48,97)'],
//             //     ['0.1', 'rgb(33,102,172)'],
//             //     ['0.2', 'rgb(67,147,195)'],
//             //     ['0.3', 'rgb(146,197,222)'],
//             //     ['0.4', 'rgb(209,229,240)'],
//             //     ['0.5', 'rgb(247,247,247)'],
//             //     ['0.6', 'rgb(253,219,199)'],
//             //     ['0.7', 'rgb(244,165,130)'],
//             //     ['0.8', 'rgb(214,96,77)'],
//             //     ['0.9', 'rgb(178,24,43)'],
//             //     ['1.0', 'rgb(103,0,31)']
//             // ],
//             reversescale: false,
//             colorbar: {
//                 title: {
//                     text: "Expression"
//                 }
//             },
//             xgap: 0.3,
//             ygap: 0.3,
//             text: dataset_text,
//             hovertemplate: "<b>Dataset: </b> %{text}<br>" +
//                 "<b>Cell-type: </b> %{x}<br>" +
//                 "<b>Expression: </b> %{z}<br>" +
//                 "<extra></extra>"
//         }];

//         var layout = {
//             autosize: true,
//             height: layout_height,
//             title: title_name,
//             annotations: [],
//             xaxis: {
//                 type: "category",
//                 showgrid: true,
//                 automargin: true,
//                 // tick0: 10,
//                 ticks: "",
//                 tickson: "boundaries",
//                 tickangle: -45,
//                 showline: true,
//                 linecolor: "#AFABAB",
//                 gridcolor: "#AFABAB",
//                 mirror: true,
//                 side: 'top'
//             },
//             yaxis: {
//                 type: "category",
//                 showgrid: true,
//                 automargin: true,
//                 // tickmode: "linear",
//                 // tick0: 25,
//                 ticks: "",
//                 tickson: "boundaries",
//                 showline: true,
//                 linecolor: "#AFABAB",
//                 gridcolor: "#AFABAB",
//                 mirror: true,
//             },
//             margin: {
//                 l: 40,
//                 t: 200
//             }
//         };

//         var filename = title_name + "_heatmap";
//         var config = {
//             responsive: false,
//             toImageButtonOptions: {
//                 format: 'png', // one of png, svg, jpeg, webp
//                 filename: filename,
//                 height: layout.height*1.2,
//                 width: 1200,
//                 scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
//             }
//         };

//         sizemax = Math.max.apply(null, data_use.percent);
//         if (data_use.celltype.length > 30) {
//             text_size = 9
//         } else {
//             text_size = 10
//         }

//         for (var i = 0; i < data_use.dataset.length; i++) {
//             for (var j = 0; j < data_use.celltype.length; j++) {
//                 var currentValue = data_use.expression[i][j];
//                 if (currentValue == null) {
//                     // var textColor = '#595959';
//                     // var zvaule = "NA";
//                     continue;
//                 } else {
//                     if (currentValue < zmin + (zmax-zmin)*2/5) {
//                         var textColor = DefaultColorBorder;
//                     } else {
//                         var textColor = '#D9D9D9';
//                     }
//                     var zvaule = currentValue;
//                     var result = {
//                         xref: 'x1',
//                         yref: 'y1',
//                         x: data_use.celltype[j],
//                         y: yvalue[i],
//                         text: zvaule,
//                         font: {
//                             family: 'Arial',
//                             size: text_size,
//                             color: textColor
//                         },
//                         showarrow: false
//                     };
//                     layout.annotations.push(result);
//                 }

//             }
//         }

//         Plotly.react(plot_id, data, layout, config);
//     });
// };

function PlotDotCPDB(data_file, title_name, plot_id) {
    Plotly.d3.json(data_file, function(error, data_use) {
        var means_array = data_use.means 
        var pvalue_array = data_use.pvalue
        var cell_array = data_use.cell_pairs
        var gene_array = data_use.gene_pairs
        // console.log(cell_array)
        // console.log(zmax_size)
        
        var sizemin, sizemax;
        sizemin = Math.min.apply(null, pvalue_array);
        sizemax = Math.max.apply(null, pvalue_array);
        var size_number, plot_height;
        if (data_use.gene_pairs.length <= 5) {
            size_number = 3;
            plot_height = 500;
        } else if (data_use.gene_pairs.length <= 20) {
            size_number = 4;
            plot_height = 30 * data_use.gene_pairs.length + 350;
        } else if (data_use.gene_pairs.length > 20 & data_use.gene_pairs.length <= 50) {
            size_number = 5;
            plot_height = 30 * data_use.gene_pairs.length + 200;
        } else {
            size_number = 6;
            plot_height = 30 * data_use.gene_pairs.length;
        }
        var size_x = [],
            size_y = [],
            size_array = [],
            size_text = [];


        var interval = (sizemax - sizemin) / (size_number - 1);
        size_x.push(0);
        size_y.push(0);
        size_array.push(sizemin + 1);
        console.log(sizemin);
        size_text.push((sizemin + 1).toFixed(1));

        for (var i = 1; i < size_number; i++) {
            size_append = sizemin + i * interval + 1;
            size_array.push(size_append);
            size_text.push(size_append.toFixed(1));
            size_x.push(0);
            size_y.push(i);
        }
        // console.log(size_array);

        var cell_x = [];
        for (var j = 0; j <= data_use.gene_pairs.length -1; j++){
            for (var i = 0; i <= data_use.cell_pairs.length -1; i++){
                cell_x.push(data_use.cell_pairs[i]);
            }
        }
        // console.log(cell_x)

        var gene_y_array = [];
        for (var j = 0; j <= data_use.gene_pairs.length -1; j++){
            gene_y_array.push(Array(data_use.cell_pairs.length).fill(data_use.gene_pairs[j]))
        }
        gene_y = [].concat.apply([], gene_y_array) 
        // console.log(gene_y)


        var desired_maximum_marker_size = 40;
        var size = pvalue_array.map(function(ele) {return ele+1});
        // console.log(size)
        var data = [{
            y: gene_y,
            x: cell_x,
            mode: 'markers',
            marker: {
                size: size,
                sizeode: 'area',
                sizeref: 2 * Math.max(...size)/desired_maximum_marker_size,

                showscale: true,
                color: means_array,
                colorscale: 'RdBu',  
                // [[0, 'rgb(200, 255, 200)'], [1, 'rgb(0, 100, 0)']],
                colorbar: {
                    thickness: 10,
                    y: 0.5,
                    ypad: 0,
                    title: 'log2(Means)',
                    titleside: 'top',
                    outlinewidth: 1,
                    outlinecolor: 'black',
                    tickfont: {
                        // family: 'Lato',
                        size: 14,
                    },
                    len: 0.5,
                    yanchor: "bottom",
                    x: 0.95,
                    xpad: 0
                }
            },
            text: data_use.means,
            hovertemplate: "<b>cell-cell: </b> %{x}<br>" +
                "<b>gene-gene: </b> %{y}<br>" +
                "<b>log2(means): </b> %{text:.3f}<br>" +
                "<b>-log10(pvalue): </b> %{marker.size:.3f}<br>" +
                "<extra></extra>",
            hoverinfo: 'text',
            showlegend: false,
        }];
        // console.log(cell_array)

        var dotsize = {
            type: 'scatter',
            x: size_x,
            y: size_y,
            xaxis: 'x2',
            yaxis: 'y2',
            mode: 'markers',
            marker: {
                size: size_array,
                sizemode: "diameter",
                sizeref: 2 * Math.max(...size)/desired_maximum_marker_size,
                // sizemin: 2,
                color: "black"
            },
            hoverinfo: 'none',
            showlegend: false,
        };
        data.push(dotsize);

        var layout = {
            autosize: true,
            height: plot_height,
            // width: 50*(data_use.cell_pairs.length),
            title: title_name, 
            annotations: [],
            hovermode: 'closest',
            xaxis: {
                range: [-0.5, data_use.cell_pairs.length-0.5],
                type: "category",
                showgrid: false,
                automargin: true,
                ticks: "",
                tickangle: -45,
                showline: true,
                gridcolor: "#AFABAB",
                mirror: true,
                side: 'top',
                domain: [0.05, 0.92]
            },
            yaxis: {
                range: [-0.5, data_use.gene_pairs.length-0.5],
                type: "category",
                showgrid: false,
                automargin: true,
                ticks: "",
                showline: true,
                gridcolor: "#AFABAB",
                mirror: true,
            },
            xaxis2: {
                range: [-0.2, 0.6],
                domain: [0.95, 1],
                showgrid: false,
                showline: false,
                zeroline: false,
                showticklabels: false,
                // mirror: "all"
            },
            yaxis2: {
                anchor: 'x2',
                domain: [0.03, 0.45],
                showgrid: false,
                showline: false,
                zeroline: false,
                showticklabels: false,
                // mirror: true
            },
            annotations: [{
                text: "-log10(pvalue)",
                showarrow: false,
                xanchor: 'left',
                x: 0.95,
                y: 0.46,
                xshift: -2.5,
                xref: 'paper',
                yref: 'paper',
            }],
            margin: {
                t: 300,
            }
        };

        for (var i = 0; i < size_array.length; i++) {
            sizetext = {
                text: size_text[i],
                showarrow: false,
                xanchor: 'left',
                font: {
                    size: 14
                },
                x: 0.15,
                y: size_y[i],
                xref: 'x2',
                yref: 'y2',
            };
            layout.annotations.push(sizetext);
        }

        Plotly.react(plot_id, data, layout);
    })
};