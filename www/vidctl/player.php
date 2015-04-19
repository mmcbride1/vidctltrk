<?php

//==============================
// REMOTE INFARED VIDEO MODULE
//==============================

 /**
   * Player
   *
   * @package    VideoPlayer
   * @subpackage None
   * @author     Matty Mc <mmcbride@spryinc.com>
   */

class Player {

    // * configuration * //

    var $vids;
    var $conf;
    
    /**
      * Construct
      *
      * Initialize the video
      * directory and set the 
      * configuration
      */

    public function __construct() {

       $this->conf = $this->conf();

       $h = $this->conf[0];

       $this->vids = $this->getVids($h);

    }
    
    /**
      * Obtain the
      * configuration
      * parameters
      */

    public function conf() {

       $conf = file('player.conf');

       for($i = 0; $i < count($conf); $i++) {

          $conf[$i] = trim($conf[$i]); 

       } 

       return $conf;
       
    }
    
    /**
      * Pack all the 
      * existing video 
      * files and make 
      * them accessible
      */

    public function getVids($dir) {

       $videos = array();

       $scan = scandir($dir);

       $hidden = array('..', '.');

       $list = array_diff($scan, $hidden);

       return $list;

    }
    
    /**
      * List the available
      * video files on 
      * the video player
      * home page
      */

    public function listVids($vids) {

       $loc = $this->conf[0];

       $cfg = $this->conf[1];

       $lnk = $this->conf[2];

       foreach($vids as $vid) {

          $locl = "$loc/$vid";

          $full = "/shared/$vid";

          echo "$cfg".$full.'"style=float:left;">'.$vid.'</a></h5>';

          echo "<a href=delete.php?file=$locl>$lnk</a><br/>";

      }
   
   }
   
   /**
     * Execute 
     * everything 
     */

    public function get() {

       $vids = $this->vids;

       return $this->listVids($vids);

    }

 }

?>
