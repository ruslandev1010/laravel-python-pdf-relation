<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use App\Models\Pdf;
use App\Models\Relation;

class PDFRegisterController extends Controller
{
    //
    public function index(Request $request)
    {
        $process = new Process(['python', app_path() . '\..\public\python\main.py']);
        $process->run();

        // executes after the command finishes
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }
        $output = json_decode($process->getOutput(), true);
        foreach($output as $key => $values)
        {
            $id1 = Pdf::where('documentName', $key)->value('id');
            if ($id1 == null) {
                $val = new Pdf;
                $val->documentName = $key;
                $val->save();
                $id1 = $val->id;
                foreach($values as $item)
                {
                    $id2 = Pdf::where('documentName', array_keys($item)[0])->value('id');
                    $val = array('documentID1' => $id1, 'documentID2' => $id2, 'strength' => array_values($item)[0], 'type' => 'D', 'status' => 'R', 'visible' => false);
                    Relation::insert($val);
                }
            }
        }
        return view('dashboard');
    }
}
