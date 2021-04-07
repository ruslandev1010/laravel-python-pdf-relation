<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\UploadedPdf;
use Illuminate\Support\Facades\Response;
use Illuminate\Support\Facades\URL;

class PDFOpenController extends Controller
{
    //
    public function pdfStream($id)
    {
        $filePath = UploadedPdf::where('documentID', $id)->value('filePath');
        return response()->json(URL::to('/') . "/storage/uploads/" . rawurlencode($filePath));
    }
}
