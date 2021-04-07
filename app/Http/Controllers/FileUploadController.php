<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Helpers\Helper;
use App\Models\File;
use App\Models\UploadedPdf;
use App\Models\Pdf;
use App\Models\Relation;

class FileUploadController extends Controller
{

    public function fileUpload(Request $req){

        $fileModel = new File;

        if($req->file()) {
            $origin_filename = $req->file->getClientOriginalName();
            $fileName = time().'_'.$origin_filename;
            $filePath = $req->file('file')->storeAs('uploads', $fileName, 'public');

            $fileModel->name = time().'_'.$origin_filename;
            $fileModel->file_path = '/storage/' . $filePath;
            $fileModel->save();

            $uppdf_maxid = UploadedPdf::max('documentID') == null ? 0 : UploadedPdf::max('documentID');

            $pdf_id = Pdf::where('documentName', $origin_filename)->value('id');

            if ($pdf_id != null) {
                $uploaded_pdfs = UploadedPdf::all();
                foreach($uploaded_pdfs as $uploaded_pdf) {
                    Relation::where('documentID1', $pdf_id)->where('documentID2', $uploaded_pdf->documentID)->update(array('visible' => true));
                    Relation::where('documentID1', $uploaded_pdf->documentID)->where('documentID2', $pdf_id)->update(array('visible' => true));
                }

                $val = new UploadedPdf;
                $val->documentID = $pdf_id;
                $val->documentName = $origin_filename;
                $val->filePath = $fileName;
                $val->save();
            } else {
                $pdf_maxid = Pdf::max('id') == null ? 0 : Pdf::max('id');
                $val = new UploadedPdf;
                $val->documentID = max($pdf_maxid + 1, $uppdf_maxid + 1);
                $val->documentName = $origin_filename;
                $val->filePath = $fileName;
                $val->save();
            }

            Helper::makeJson();

            return response()->json('success');
        }
    }
}
