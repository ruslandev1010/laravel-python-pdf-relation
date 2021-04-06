<?php // Code within app\Helpers\Helper.php

namespace App\Helpers;
use App\Models\Relation;
use App\Models\UploadedPdf;

class Helper
{
    public static function makeJson()
    {

      //Load uploaded_pdfs table and relations table
      $uppdfs = UploadedPdf::all();
      $nodes = array();
      foreach($uppdfs as $uppdf) {
          $node = array();
          $node['name'] = "";
          $node['label'] = $uppdf->documentName;
          $node['id'] = $uppdf->documentID;
          array_push($nodes, $node);
      }

      $relations = Relation::all();
      $links = array();
      foreach($relations as $relation) {
          if ($relation->type == "D" && $relation->visible == true) {
              $link = array();
              $link['source'] = $relation->documentID1;
              $link['target'] = $relation->documentID2;
              $link['type'] = (string) $relation->strength;
              array_push($links, $link);
          }
      }
      //dd($links);
      $json_array = array();
      $json_array['nodes'] = $nodes;
      $json_array['links'] = $links;
      $json = json_encode($json_array);
      $bytes = file_put_contents("graph.json", $json);
    }
}