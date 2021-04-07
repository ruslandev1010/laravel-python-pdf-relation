$(document).ready(function(){

  var colors = d3.scaleOrdinal(d3.schemeCategory10);
  var svg = d3.select("svg"),
  width = +svg.attr("width"),
  height = +svg.attr("height"),
  node,
  link;

  var simulation = d3.forceSimulation()
  .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(200).strength(1))
  .force("charge", d3.forceManyBody())
  .force("center", d3.forceCenter(width / 2, height / 2));



  //restart();
  d3.json("graph.json", function (error, graph) {
      if (error) throw error;
      //console.log(graph.links);
      update(graph.links, graph.nodes);
  })

  $("#file").change(function(){
    var fd = new FormData(this.form);
    var files = $('#file')[0].files;

    // Check file selected or not
    if(files.length > 0 ){
        fd.append('file',files[0]);
        $.ajaxSetup({
          headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
          }
        });
        $.ajax({
          url: 'http://loc.relation.com/upload-file',
          type: 'POST',
          data: fd,
          dataType: 'json',
          cache: false,
          contentType: false,
          processData: false,
          success: function(response){
              if(response != 0){
               // console.log("successed");
                restart();
              }else{
               // console.log("failed");
              }
          },
          error: function(error) {
            //console.log('error');
          }
        });
    }else{
      alert("Please select a file.");
    }
  });

  function restart() {
    d3.json("graph.json", function (error, graph) {
      if (error) throw error;
      //console.log(graph.links);
      svg.selectAll('*').remove();
      simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(200).strength(1))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));
      svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':13,
            'refY':0,
            'orient':'auto',
            'markerWidth':13,
            'markerHeight':13,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');

      update(graph.links, graph.nodes);
      simulation.alpha(1).restart();
    })
  }
  function update(links, nodes) {
    link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end','url(#arrowhead)')

    link.append("title")
        .text(function (d) {return d.type;});

    edgepaths = svg.selectAll(".edgepath")
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'id': function (d, i) {return 'edgepath' + i}
        })
        .style("pointer-events", "none");

    edgelabels = svg.selectAll(".edgelabel")
        .data(links)
        .enter()
        .append('text')
        .style("pointer-events", "none")
        .attrs({
            'class': 'edgelabel',
            'id': function (d, i) {return 'edgelabel' + i},
            'font-size': 10,
            'fill': '#aaa'
        });

    edgelabels.append('textPath')
        .attr('xlink:href', function (d, i) {return '#edgepath' + i})
        .style("text-anchor", "middle")
        .style("pointer-events", "none")
        .attr("startOffset", "50%")
        .text(function (d) {return d.type});

    node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .on("dblclick", dblclick)
        .on("contextmenu", rightclick)
        .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended)

        );

    node.append("circle")
        .attr("r", 10)
        .style("fill", function (d, i) {return colors(i);})

    node.append("title")
        .text(function (d) {return d.id;});

    node.append("text")
        .attr("dy", -3)
        .text(function (d) {return d.name+":"+d.label;});

    simulation
        .nodes(nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(links);
  }

  function ticked() {
      link
          .attr("x1", function (d) {return d.source.x;})
          .attr("y1", function (d) {return d.source.y;})
          .attr("x2", function (d) {return d.target.x;})
          .attr("y2", function (d) {return d.target.y;});

      node
          .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

      edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
      });

      edgelabels.attr('transform', function (d) {
          if (d.target.x < d.source.x) {
              var bbox = this.getBBox();

              rx = bbox.x + bbox.width / 2;
              ry = bbox.y + bbox.height / 2;
              return 'rotate(180 ' + rx + ' ' + ry + ')';
          }
          else {
              return 'rotate(0)';
          }
      });
  }

  function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      //d3.select(this).classed("fixed", d.fixed = false);
      //simulation.force("link", null).force("charge", null).force("center", null);
      d.fx = d.x;
      d.fy = d.y;
  }

  function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
      fix_nodes(d);
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
  }

  // Preventing other nodes from moving while dragging one node
  function fix_nodes(this_node) {
    node.each(function(d){
        if (this_node != d){
            d.fx = d.x;
            d.fy = d.y;
        }
    });
  }

  function dblclick(d) {
    $('#current-document').val(d.label);
    $.ajax({
      type: "GET",
      url: "/related-document/" + d.id,
      success: function(data) {
        $('#related-document').empty();
        for (i = 0; i < data.length; i++) {
          $('#related-document').append(`<option value="${data[i].documentName}"> ${data[i].documentName} </option>`);
        }
        $('#linkModal').modal('show');
      },
      error: function(error) {
        //console.log('error');
      }
    });
  }

  function rightclick(d) {
    d3.event.preventDefault();
    $.ajax({
      type: "GET",
      url: "/open/" + d.id,
      success: function(data) {
        console.log(data);
        $('#pdflink').attr("href", data);
        console.log($('#pdflink').attr("href"));
        $('#pdflink')[0].click();
        console.log('success');
      },
      error: function(error) {
        console.log('error');
      }
    });
  }

  $('#removeBtn').click(function() {
    $.ajaxSetup({
      headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
      }
    });
    $.ajax({
      type: 'POST',
      url:  '/related-document',
      data: {
        currentDocument: $('#current-document').val(),
        relatedDocument: $('#related-document option:selected').text()
      },
      dataType: 'json',
      success: function(response) {
        $('#linkModal').modal('hide');
        if(response != 0) {
         // console.log("success");
          restart();
        }else{
         // console.log("failed");
        }
      },
      error: function(error) {
        //console.log('error');
      }
    });
  })
});

//val(data[i].documentName);