<?php

namespace App\Http\Controllers;

use App\Helpers\Helper;
use Illuminate\Http\Request;
use App\Models\Relation;
use App\Models\UploadedPdf;

class RelatedDocumentsController extends Controller
{
    //
    public function getRelatedDocuments($id)
    {
        $related_documents = Relation::where('documentID1', $id)->where('visible', true)->get();
        $array = array();
        foreach($related_documents as $related_document) {
            $id = $related_document->documentID2;
            $name = UploadedPdf::where('documentID', $id)->value('documentName');
            $value = array();
            $value['id'] = $id;
            $value['documentName'] = $name;
            array_push($array, $value);
        }
        return response()->json($array);
    }

    public function removeRelatedDocument(Request $request)
    {
        $id1 = UploadedPdf::where('documentName', $request->currentDocument)->value('documentID');
        $id2 = UploadedPdf::where('documentName', $request->relatedDocument)->value('documentID');
        Relation::where('documentID1', $id1)->where('documentID2', $id2)->update(array('visible' => false));
        Relation::where('documentID1', $id2)->where('documentID2', $id1)->update(array('visible' => false));
        Helper::makeJson();
        return response()->json('success');
    }
}
