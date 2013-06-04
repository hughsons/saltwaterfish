
function click_ship()
{
//return true;
}

function toggleoff()
{  
var obj1;
  var divs = document.getElementsByTagName("div");
  for (var x = 0; x < divs.length; ++x)
  {
    if ((divs[x].id.indexOf("shUSPS") >= 0) || (divs[x].id.indexOf("shUPS") >= 0) || (divs[x].id.indexOf("shCA Post") >= 0) || (divs[x].id.indexOf("shFEDEX") >= 0))
      obj1=document.getElementById(divs[x].id);
	if (obj1!=undefined) {
	obj1.style.display = 'none';
	}
  }    
} 


function addLoadEvent(func) {
//Add event to the onload stack
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}


function toggleoff_mul(shipment)
{  
var obj1;
  var divs = document.getElementsByTagName("div");
  for (var x = 0; x < divs.length; ++x)
  {
    if ((divs[x].id.indexOf("sh" + shipment + "USPS") >= 0) || (divs[x].id.indexOf("sh" + shipment + "UPS") >= 0) || (divs[x].id.indexOf("sh" + shipment + "CA Post") >= 0) || (divs[x].id.indexOf("sh" + shipment + "FEDEX") >= 0))
      obj1=document.getElementById(divs[x].id);
	if (obj1!=undefined) {
	obj1.style.display = 'none';
	}
  }    
} 


function toggle(itemname)
{
var obj1;
obj1=document.getElementById(itemname);

if (obj1!=undefined) {

  if (obj1.style.display == 'none')
  {obj1.style.display = ''
  }
  else
  obj1.style.display = 'none'
} }


function toggleProdOptions(itemname)
{
var obj1;
obj1=document.getElementById(itemname);

if (obj1!=undefined) {

  if (obj1.style.display == 'none')
  {obj1.style.display = ''
  }
  else
  obj1.style.display = 'none'
} }


function doclick()
{

}

function filladdress_form(save_address,formname,type){

		var frm = eval('document.'+formname);
		
		var oElement = eval(save_address)

		if (oElement.selectedIndex < 0) oElement.selectedIndex = 0;

		if (oElement.selectedIndex > -1) {
			var oValues = oElement.options[oElement.selectedIndex].value.split("::");
			
			eval("document."+formname+"."+type+"_address").value = oValues[0];
			eval("document."+formname+"."+type+"_firstname").value = oValues[1];
			eval("document."+formname+"."+type+"_lastname").value = oValues[2];
			eval("document."+formname+"."+type+"_address2").value = oValues[3];
			eval("document."+formname+"."+type+"_city").value = oValues[4];
			eval("document."+formname+"."+type+"_zip").value = oValues[5];
			eval("document."+formname+"."+type+"_phone").value = oValues[8];
			eval("document."+formname+"."+type+"_company").value = oValues[9];
			
			initCountry(oValues[7],oValues[6],type+'_state',type+'_country');	//Inside admin/state_countryjs.asp
			
		}
}
	
function filladdress(save_address){

		filladdress_form(save_address, save_address.form.name, 'shipping');
		return;
		
		var frm = document.addresslist;
		
		var oElement = eval(save_address)

		if (oElement.selectedIndex < 0) oElement.selectedIndex = 0;

		if (oElement.selectedIndex > -1) {
			var oValues = oElement.options[oElement.selectedIndex].value.split("::");
			
			eval("document.checkoutform.shipping_address").value = oValues[0];
			eval("document.checkoutform.shipping_firstname").value = oValues[1];
			eval("document.checkoutform.shipping_lastname").value = oValues[2];
			eval("document.checkoutform.shipping_address2").value = oValues[3];
			eval("document.checkoutform.shipping_city").value = oValues[4];
			eval("document.checkoutform.shipping_zip").value = oValues[5];
			eval("document.checkoutform.shipping_state").value = oValues[6];
			eval("document.checkoutform.shipping_country").value = oValues[7];
			eval("document.checkoutform.shipping_phone").value = oValues[8];
			eval("document.checkoutform.shipping_company").value = oValues[9];
			
		} else {
			//alert("You must select an address to fill.");
		}
	}



var isSubmitComplete = false;
var paymentfound=0;
var bolCheckSubmitted_validation = true;	//On the page, set it to false if you don't want to check for form already submitted.

    function submitForm(bolCheckSubmitted){
		
         if (!isSubmitComplete || !bolCheckSubmitted_validation){
		
		   isSubmitComplete = true;
                  
              	   return true;
			  
         }else{
              alert("Form already submitted please wait...");
	      return false;
         }
    }




/*
  -------------------------------------------------------------------------
		      javascript Form Validator (gen_validatorv31.js)
              Version 3.1
	Copyright (C) 2003-2008 javascript-Coder.com. All rights reserved.
	You can freely use this script in your Web pages.
	You may adapt this script for your own needs, provided these opening credit
    lines are kept intact.
		
	The Form validation script is distributed free from javascript-Coder.com
	For updates, please visit:
	http://www.javascript-coder.com/html-form/javascript-form-validation.phtml
	
	Questions & comments please send to support@javascript-coder.com
  -------------------------------------------------------------------------  
*/
function Validator(frmname)
{
  this.formobj=document.forms[frmname];
	if(!this.formobj)
	{
	  alert("Error: couldnot get Form object "+frmname);
		return;
	}
	if(this.formobj.onsubmit)
	{
	 this.formobj.old_onsubmit = this.formobj.onsubmit;
	 this.formobj.onsubmit=null;
	}
	else
	{
	 this.formobj.old_onsubmit = null;
	}
	this.formobj._sfm_form_name=frmname;
	this.formobj.onsubmit=form_submit_handler;
	this.addValidation = add_validation;
	this.setAddnlValidationFunction=set_addnl_vfunction;
	this.clearAllValidations = clear_all_validations;
    this.disable_validations = false;//new
    document.error_disp_handler = new sfm_ErrorDisplayHandler();
    this.EnableOnPageErrorDisplay=validator_enable_OPED;
	this.EnableOnPageErrorDisplaySingleBox=validator_enable_OPED_SB;
    this.show_errors_together=true;
    this.EnableMsgsTogether=sfm_enable_show_msgs_together;
}
function set_addnl_vfunction(functionname)
{
  this.formobj.addnlvalidation = functionname;
}
function sfm_enable_show_msgs_together()
{
    this.show_errors_together=true;
    this.formobj.show_errors_together=true;
}
function clear_all_validations()
{
	for(var itr=0;itr < this.formobj.elements.length;itr++)
	{
		this.formobj.elements[itr].validationset = null;
	}
}
function form_submit_handler()
{
   var bRet = true;
    document.error_disp_handler.clear_msgs();
	for(var itr=0;itr < this.elements.length;itr++)
	{
		if(this.elements[itr].validationset &&
	   !this.elements[itr].validationset.validate())
		{
		  bRet = false;
		}
        if(!bRet && !this.show_errors_together)
        {
          break;
        }
	}
    if(!bRet)
    {
      document.error_disp_handler.FinalShowMsg();
      return false;
    }

	if(this.addnlvalidation)
	{
	  str =" var ret = "+this.addnlvalidation+"()";
	  eval(str);
    if(!ret) return ret;
	}
	return true;
}
function add_validation(itemname,descriptor,errstr)
{
	var condition = null;
	if(arguments.length > 3)
	{
	 condition = arguments[3]; 
	}
	
  if(!this.formobj)
	{
		alert("Error: The form object is not set properly");
		return;
	}//if
	var itemobj = this.formobj[itemname];

    if(itemobj.length && isNaN(itemobj.selectedIndex) )
    //for radio button; don't do for 'select' item
	{
		itemobj = itemobj[0];
	}	
	if(!itemobj)
	{
		alert("Error: Couldnot get the input object named: "+itemname);
		return;
	}
	if(!itemobj.validationset)
	{
		itemobj.validationset = new ValidationSet(itemobj,this.show_errors_together);
	}
	itemobj.validationset.add(descriptor,errstr,condition);
    itemobj.validatorobj=this;
}
function validator_enable_OPED()
{
    document.error_disp_handler.EnableOnPageDisplay(false);
}

function validator_enable_OPED_SB()
{
	document.error_disp_handler.EnableOnPageDisplay(true);
}
function sfm_ErrorDisplayHandler()
{
  this.msgdisplay = new AlertMsgDisplayer();
  this.EnableOnPageDisplay= edh_EnableOnPageDisplay;
  this.ShowMsg=edh_ShowMsg;
  this.FinalShowMsg=edh_FinalShowMsg;
  this.all_msgs=new Array();
  this.clear_msgs=edh_clear_msgs;
}
function edh_clear_msgs()
{
    this.msgdisplay.clearmsg(this.all_msgs);
    this.all_msgs = new Array();
}
function edh_FinalShowMsg()
{
    this.msgdisplay.showmsg(this.all_msgs);
}
function edh_EnableOnPageDisplay(single_box)
{
	if(true == single_box)
	{
		this.msgdisplay = new SingleBoxErrorDisplay();
	}
	else
	{
		this.msgdisplay = new DivMsgDisplayer();		
	}
}
function edh_ShowMsg(msg,input_element)
{
	
   var objmsg = new Array();
   objmsg["input_element"] = input_element;
   objmsg["msg"] =  msg;
   this.all_msgs.push(objmsg);
}
function AlertMsgDisplayer()
{
  this.showmsg = alert_showmsg;
  this.clearmsg=alert_clearmsg;
}
function alert_clearmsg(msgs)
{

}
function alert_showmsg(msgs)
{
    var whole_msg="";
    var first_elmnt=null;
    for(var m in msgs)
    {
        if(null == first_elmnt)
        {
            first_elmnt = msgs[m]["input_element"];
        }
        if(msgs[m]["msg"] != undefined)
			whole_msg += msgs[m]["msg"] + "\n";
    }
	
    alert(whole_msg);

    if(null != first_elmnt)
    {
        first_elmnt.focus();
    }
}
function sfm_show_error_msg(msg,input_elmt)
{
    document.error_disp_handler.ShowMsg(msg,input_elmt);
}
function SingleBoxErrorDisplay()
{
 this.showmsg=sb_div_showmsg;
 this.clearmsg=sb_div_clearmsg;
}

function sb_div_clearmsg(msgs)
{
	var divname = form_error_div_name(msgs);
	show_div_msg(divname,"");
}

function sb_div_showmsg(msgs)
{
	var whole_msg="<ul>\n";
	for(var m in msgs)
    {
        whole_msg += "<li>" + msgs[m]["msg"] + "</li>\n";
    }
	whole_msg += "</ul>";
	var divname = form_error_div_name(msgs);
	show_div_msg(divname,whole_msg);
}
function form_error_div_name(msgs)
{
	var input_element= null;

	for(var m in msgs)
	{
	 input_element = msgs[m]["input_element"];
	 if(input_element){break;}
	}

	var divname ="";
	if(input_element)
	{
	 divname = input_element.form._sfm_form_name + "_errorloc";
	}

	return divname;
}
function DivMsgDisplayer()
{
 this.showmsg=div_showmsg;
 this.clearmsg=div_clearmsg;
}
function div_clearmsg(msgs)
{
    for(var m in msgs)
    {
        var divname = element_div_name(msgs[m]["input_element"]);
        show_div_msg(divname,"");
    }
}
function element_div_name(input_element)
{
  var divname = input_element.form._sfm_form_name + "_" + 
                   input_element.name + "_errorloc";

  divname = divname.replace(/[\[\]]/gi,"");

  return divname;
}
function div_showmsg(msgs)
{
    var whole_msg;
    var first_elmnt=null;
    for(var m in msgs)
    {
        if(null == first_elmnt)
        {
            first_elmnt = msgs[m]["input_element"];
        }
        var divname = element_div_name(msgs[m]["input_element"]);
        show_div_msg(divname,msgs[m]["msg"]);
    }
    if(null != first_elmnt)
    {
        first_elmnt.focus();
    }
}
function show_div_msg(divname,msgstring)
{
	if(divname.length<=0) return false;

	if(document.layers)
	{
		divlayer = document.layers[divname];
        if(!divlayer){return;}
		divlayer.document.open();
		divlayer.document.write(msgstring);
		divlayer.document.close();
	}
	else
	if(document.all)
	{
		divlayer = document.all[divname];
        if(!divlayer){return;}
		divlayer.innerHTML=msgstring;
	}
	else
	if(document.getElementById)
	{
		divlayer = document.getElementById(divname);
        if(!divlayer){return;}
		divlayer.innerHTML =msgstring;
	}
	divlayer.style.visibility="visible";	
	return false;
}
function ValidationDesc(inputitem,desc,error,condition)
{
  this.desc=desc;
	this.error=error;
	this.itemobj = inputitem;
	this.condition = condition;
	this.validate=vdesc_validate;
}
function vdesc_validate()
{
	if(this.condition != null )
	{
		if(!eval(this.condition))
		{
			return true;
		}
	}
	if(!validateInput(this.desc,this.itemobj,this.error))
	{
		this.itemobj.validatorobj.disable_validations=true;
		this.itemobj.focus();
		return false;
	}
	return true;
}
function ValidationSet(inputitem,msgs_together)
{
    this.vSet=new Array();
	this.add= add_validationdesc;
	this.validate= vset_validate;
	this.itemobj = inputitem;
    this.msgs_together = msgs_together;
}
function add_validationdesc(desc,error,condition)
{
  this.vSet[this.vSet.length]= 
  new ValidationDesc(this.itemobj,desc,error,condition);
}
function vset_validate()
{
    var bRet = true;
    for(var itr=0;itr<this.vSet.length;itr++)
    {
        bRet = bRet && this.vSet[itr].validate();
        if(!bRet && !this.msgs_together)
        {
            break;
        }
    }
    return bRet;
}
function validateEmail(email)
{
    var splitted = email.match("^(.+)@(.+)$");
    if(splitted == null) return false;
    if(splitted[1] != null )
    {
      var regexp_user=/^\"?[\w-_\.]*\"?$/;
      if(splitted[1].match(regexp_user) == null) return false;
    }
    if(splitted[2] != null)
    {
      var regexp_domain=/^[\w-\.]*\.[A-Za-z]{2,4}$/;
      if(splitted[2].match(regexp_domain) == null) 
      {
	    var regexp_ip =/^\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]$/;
	    if(splitted[2].match(regexp_ip) == null) return false;
      }// if
      return true;
    }
return false;
}

function IsCheckSelected(objValue,chkValue)
{
    var selected=false;
	var objcheck = objValue.form.elements[objValue.name];
    if(objcheck.length)
	{
		var idxchk=-1;
		for(var c=0;c < objcheck.length;c++)
		{
		   if(objcheck[c].value == chkValue)
		   {
		     idxchk=c;
			 break;
		   }//if
		}//for
		if(idxchk>= 0)
		{
		  if(objcheck[idxchk].checked=="1")
		  {
		    selected=true;
		  }
		}//if
	}
	else
	{
		if(objValue.checked == "1")
		{
			selected=true;
		}//if
	}//else	

	return selected;
}
function TestDontSelectChk(objValue,chkValue,strError)
{
	var pass = true;
	pass = IsCheckSelected(objValue,chkValue)?false:true;

	if(pass==false)
	{
     if(!strError || strError.length ==0) 
        { 
        	strError = "Can't Proceed as you selected "+objValue.name;  
        }//if			  
	  sfm_show_error_msg(strError,objValue);
	  
	}
    return pass;
}
function TestShouldSelectChk(objValue,chkValue,strError)
{
	var pass = true;

	pass = IsCheckSelected(objValue,chkValue)?true:false;

	if(pass==false)
	{
     if(!strError || strError.length ==0) 
        { 
        	strError = "You should select"+objValue.name;  
        }//if			  
	  sfm_show_error_msg(strError,objValue);
	  
	}
    return pass;
}
function TestRequiredInput(objValue,strError)
{
 var ret = true;
    if(eval(objValue.value.length) == 0) 
    { 
       if(!strError || strError.length ==0) 
       { 
         strError = objValue.name + " : Required Field"; 
       }//if 
       sfm_show_error_msg(strError,objValue); 
       ret=false; 
    }//if 
return ret;
}
function TestMaxLen(objValue,strMaxLen,strError)
{
 var ret = true;
    if(eval(objValue.value.length) > eval(strMaxLen)) 
    { 
      if(!strError || strError.length ==0) 
      { 
        strError = objValue.name + " : "+ strMaxLen +" characters maximum "; 
      }//if 
      sfm_show_error_msg(strError,objValue); 
      ret = false; 
    }//if 
return ret;
}
function TestMinLen(objValue,strMinLen,strError)
{
 var ret = true;
    if(eval(objValue.value.length) <  eval(strMinLen)) 
    { 
      if(!strError || strError.length ==0) 
      { 
        strError = objValue.name + " : " + strMinLen + " characters minimum  "; 
      }//if               
      sfm_show_error_msg(strError,objValue); 
      ret = false;   
    }//if 
return ret;
}
function TestInputType(objValue,strRegExp,strError,strDefaultError)
{
   var ret = true;

    var charpos = objValue.value.search(strRegExp); 
    if(objValue.value.length > 0 &&  charpos >= 0) 
    { 
     if(!strError || strError.length ==0) 
      { 
        strError = strDefaultError;
      }//if 
      sfm_show_error_msg(strError,objValue); 
      ret = false; 
    }//if 
 return ret;
}
function TestEmail(objValue,strError)
{
var ret = true;
     if(objValue.value.length > 0 && !validateEmail(objValue.value)	 ) 
     { 
       if(!strError || strError.length ==0) 
       { 
          strError = objValue.name+": Enter a valid Email address "; 
       }//if                                               
       sfm_show_error_msg(strError,objValue); 
       ret = false; 
     }//if 
return ret;
}
function TestLessThan(objValue,strLessThan,strError)
{
var ret = true;
	  if(isNaN(objValue.value)) 
	  { 
	    sfm_show_error_msg(objValue.name +": Should be a number ",objValue); 
	    ret = false; 
	  }//if 
	  else
	  if(eval(objValue.value) >=  eval(strLessThan)) 
	  { 
	    if(!strError || strError.length ==0) 
	    { 
	      strError = objValue.name + " : value should be less than "+ strLessThan; 
	    }//if               
	    sfm_show_error_msg(strError,objValue); 
	    ret = false;                 
	   }//if   
return ret;          
}
function TestGreaterThan(objValue,strGreaterThan,strError)
{
var ret = true;
     if(isNaN(objValue.value)) 
     { 
       sfm_show_error_msg(objValue.name+": Should be a number ",objValue); 
       ret = false; 
     }//if 
	 else
     if(eval(objValue.value) <=  eval(strGreaterThan)) 
      { 
        if(!strError || strError.length ==0) 
        { 
          strError = objValue.name + " : value should be greater than "+ strGreaterThan; 
        }//if               
        sfm_show_error_msg(strError,objValue);  
        ret = false;
      }//if  
return ret;           
}
function TestRegExp(objValue,strRegExp,strError)
{
var ret = true;
    if( objValue.value.length > 0 && 
        !objValue.value.match(strRegExp) ) 
    { 
      if(!strError || strError.length ==0) 
      { 
        strError = objValue.name+": Invalid characters found "; 
      }//if                                                               
      sfm_show_error_msg(strError,objValue); 
      ret = false;                   
    }//if 
return ret;
}
function TestDontSelect(objValue,dont_sel_value,strError)
{
var ret = true;
     if(objValue.value == null) 
     { 
       sfm_show_error_msg("Error: dontselect command for non-select Item",objValue); 
       ret = false; 
     } 
	 else
     if(objValue.value == dont_sel_value) 
     { 
      if(!strError || strError.length ==0) 
       { 
        strError = objValue.name+": Please Select one option "; 
       }//if                                                               
       sfm_show_error_msg(strError,objValue); 
       ret =  false;                                   
      } 
return ret;
}
function TestSelectOneRadio(objValue,strError)
{
	var objradio = objValue.form.elements[objValue.name];
	var one_selected=false;
	for(var r=0;r < objradio.length;r++)
	{
	  if(objradio[r].checked == "1")
	  {
	  	one_selected=true;
		break;
	  }
	}
	if(false == one_selected)
	{
      if(!strError || strError.length ==0) 
       {
	    strError = "Please select one option from "+objValue.name;
	   }	
	  sfm_show_error_msg(strError,objValue);
	}
return one_selected;
}

function validateInput(strValidateStr,objValue,strError) 
{ 
    var ret = true;
    var epos = strValidateStr.search("="); 
    var  command  = ""; 
    var  cmdvalue = ""; 
    if(epos >= 0) 
    { 
     command  = strValidateStr.substring(0,epos); 
     cmdvalue = strValidateStr.substr(epos+1); 
    } 
    else 
    { 
     command = strValidateStr; 
    } 

    switch(command) 
    { 
        case "req": 
        case "required": 
         { 
		   ret = TestRequiredInput(objValue,strError)
           break;             
         }//case required 
        case "maxlength": 
        case "maxlen": 
          { 
			 ret = TestMaxLen(objValue,cmdvalue,strError)
             break; 
          }//case maxlen 
        case "minlength": 
        case "minlen": 
           { 
			 ret = TestMinLen(objValue,cmdvalue,strError)
             break; 
            }//case minlen 
        case "alnum": 
        case "alphanumeric": 
           { 
				ret = TestInputType(objValue,"[^A-Za-z0-9]",strError, 
						objValue.name+": Only alpha-numeric characters allowed ");
				break; 
           }
        case "alnum_s": 
        case "alphanumeric_space": 
           { 
				ret = TestInputType(objValue,"[^A-Za-z0-9\\s]",strError, 
						objValue.name+": Only alpha-numeric characters and space allowed ");
				break; 
           }		   
        case "num": 
        case "numeric": 
           { 
                ret = TestInputType(objValue,"[^0-9]",strError, 
						objValue.name+": Only digits allowed ");
                break;               
           }
        case "alphabetic": 
        case "alpha": 
           { 
                ret = TestInputType(objValue,"[^A-Za-z]",strError, 
						objValue.name+": Only alphabetic characters allowed ");
                break; 
           }
        case "alphabetic_space": 
        case "alpha_s": 
           { 
                ret = TestInputType(objValue,"[^A-Za-z\\s]",strError, 
						objValue.name+": Only alphabetic characters and space allowed ");
                break; 
           }
        case "email": 
          { 
			   ret = TestEmail(objValue,strError);
               break; 
          }
		case "phone": 
		{ 

			ret = validatePhone(objValue,strError);		
			break; 
		}
		         
        case "lt": 
        case "lessthan": 
         { 
    	      ret = TestLessThan(objValue,cmdvalue,strError);
              break; 
         }
        case "gt": 
        case "greaterthan": 
         { 
			ret = TestGreaterThan(objValue,cmdvalue,strError);
            break; 
         }//case greaterthan 
        case "regexp": 
         { 
			ret = TestRegExp(objValue,cmdvalue,strError);
           break; 
         }
        case "dontselect": 
         { 
			 ret = TestDontSelect(objValue,cmdvalue,strError)
             break; 
         }
		case "dontselectchk":
		{
			ret = TestDontSelectChk(objValue,cmdvalue,strError)
			break;
		}
		case "shouldselchk":
		{
			ret = TestShouldSelectChk(objValue,cmdvalue,strError)
			break;
		}
		case "selone_radio":
		{
			ret = TestSelectOneRadio(objValue,strError);
		    break;
		}		 
    }//switch 
	return ret;
}


function TestEmail(objValue,strError)
{
var ret = true;
     if(objValue.value.length > 0 && !validateEmail(objValue.value)	 ) 
     { 
       if(!strError || strError.length ==0) 
       { 
          strError = objValue.name+": Enter a valid Email address "; 
       }//if                                               
       sfm_show_error_msg(strError,objValue); 
       ret = false; 
     }//if 
return ret;
}

function validatePhone(objValue,strError)
{

	// a very simple email validation checking. 
	// you can add more complex email checking if it helps 
	var phonenumber = objValue.value;
	var ret = false;

    if(phonenumber.length <= 0)
	{
	  ret = false;
	}
	
	var digits = "0123456789";
	var phoneNumberDelimiters = "()- ";
	var validWorldPhoneChars = phoneNumberDelimiters + "+";
	var minDigitsInIPhoneNumber = 10;

	s=stripCharsInBag(phonenumber,validWorldPhoneChars);
	if (isInteger(s) && s.length >= minDigitsInIPhoneNumber)
	{
	  ret = true;
	}

    if(!strError || strError.length ==0) 
    { 
        strError = objValue.name+": Phone number is invalid "; 
    }
    
    if (!ret)
		sfm_show_error_msg(strError,objValue); 	
	
	return ret;
}

function stripCharsInBag(s, bag)
{   var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++)
    {   
        // Check that current character isn't whitespace.
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function isInteger(s)
{   var i;
    for (i = 0; i < s.length; i++)
    {   
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

function VWZ_IsListItemSelected(listname,value)
{
 for(var i=0;i < listname.options.length;i++)
 {
  if(listname.options[i].selected == true &&
   listname.options[i].value == value) 
   {
     return true;
   }
 }
 return false;
}
function VWZ_IsChecked(objcheck,value)
{
 if(objcheck.length)
 {
     for(var c=0;c < objcheck.length;c++)
     {
       if(objcheck[c].checked == "1" && 
	     objcheck[c].value == value)
       {
        return true; 
       }
     }
 }
 else
 {
  if(objcheck.checked == "1" )
   {
    return true; 
   }    
 }
 return false;
}
/*
	Copyright (C) 2003-2008 javascript-Coder.com . All rights reserved.
*/


















// FOR MAILING LIST
//////////////////////////////////////////////////////////////////////////////////////////
function mailing_list()
{
if (document.mailing.email.value=="")
{
alert("Please enter an email!");
return false;
}
return true;
}


// FOR CHECKOUT 1
//////////////////////////////////////////////////////////////////////////////////////////
function Changeshippingtype(stype) 
{
		if (stype == 1)
		{
			
			country_object="document.checkoutform.shipping_country";
			if (eval(country_object)) 
			{
			document.checkoutform.shipping_type[0].checked=true;
			select_field(country_object,"US");
			}
			
		}
		else
		{
			document.checkoutform.shipping_type[1].checked=true;
		}


}


function select_field(objectname,objvalue)
{
for (i=0;i<=(eval(objectname+'.length')-1);i++)
{
if ((eval(objectname + '.options[' + i + '].value'))==objvalue)
{
eval(objectname+'.options['+i+'].selected=true');
}
else{
eval(objectname+'.options['+i+'].selected=false');
}}}
//////////////////////////////////////////////////////////////////////////////////////////

// FOR CHECKOUT 2
//////////////////////////////////////////////////////////////////////////////////////////
function checkselectedshipping()
{

}
//////////////////////////////////////////////////////////////////////////////////////////

// FOR CHECKOUT 3
//////////////////////////////////////////////////////////////////////////////////////////


//document.billing.billing_country.value='[shipping_country]';

// For each option in country drop down... find index of shipping country, and select it!

function select_field(objectname,objvalue)
{
for (i=0;i<=(eval(objectname+'.length')-1);i++)
{
if ((eval(objectname + '.options[' + i + '].value'))==objvalue)
{
eval(objectname+'.options['+i+'].selected=true');
}
else{
eval(objectname+'.options['+i+'].selected=false');
}}}

function Changeshippingtypeb(stype) 
{
		if (stype == 1)
		{
			if (eval(country_object)) 
			{
			document.billing.billing_type[0].checked=true;
			country_object="document.billing.billing_country";
			select_field(country_object,"US");
			}
		}
		else
		{
			document.billing.billing_type[1].checked=true;
		}
}
//////////////////////////////////////////////////////////////////////////////////////////

function checkreq_questions1()
{
	 var frm = document.forms["checkoutform"];
	 var fieldval;
  
  
  	
    for (var i = 0; i<frm.elements.length; i++) {
        if ((frm.elements[i].name.indexOf('OPTREQ') > -1)) {
            
            
            if (frm.elements[i].type == 'checkbox') 
            {
           	if ((frm.elements[i].checked)!=true) 
           	{alert ("Please fill in all required fields.");
            frm.elements[i].focus();   
            return false; 
            }
           	
            
           	}
            else
         	{
            if (frm.elements[i].value <='')
            {alert ("Please fill in all required fields.");
            frm.elements[i].focus();         
            return false;
            }
            
            }
            
        	
        }
    }
  
  return submitForm();

   }

function checkreq_questions3()
{
	 var frm = document.forms["billing"];
	 var fieldval;
  
  
  	
    for (var i = 0; i<frm.elements.length; i++) {
        if ((frm.elements[i].name.indexOf('OPTREQ') > -1) && (frm.elements[i].name.indexOf('cq') > -1)) {
            
            
            if (frm.elements[i].type == 'checkbox') 
            {
           	if ((frm.elements[i].checked)!=true) 
           	{alert ("Please fill in all required fields.");
            frm.elements[i].focus();   
            return false; 
            }
           	
            
           	}
            else
         	{
            if (frm.elements[i].value <='')
            {alert ("Please fill in all required fields.");
            frm.elements[i].focus();         
            return false;
            }
            
            }
            
        	
        }
    }
  
  

   }
   	
function checkreq_questions2()
{
	 var frm = document.forms["pickship"];
	 var fieldval;
  
  
  	
    for (var i = 0; i<frm.elements.length; i++) {
        if ((frm.elements[i].name.indexOf('OPTREQ') > -1) ) {
            
            
            if (frm.elements[i].type == 'checkbox') 
            {
           	if ((frm.elements[i].checked)!=true) 
           	{alert ("Please fill in all required fields.");
            frm.elements[i].focus();   
            return false; 
            }
           	
            
           	}
            else
         	{
            if (frm.elements[i].value <='')
            {alert ("Please fill in all required fields.");
            frm.elements[i].focus();         
            return false;
            }
            
            }
            
        	
        }
    }
  
  return submitForm();

   }
	



function checkotherreqfields()
{
	var frm = document.forms["billing"];
	var fieldval;
	var paymentinfo;
	var paymentsel;

	var maxpmethods=0;
  
  if (frm.payment != 'undefined' && frm.payment != null)
	if (frm.payment.length!='undefined')
		maxpmethods=frm.payment.length;

if (maxpmethods>0) 
{
	// Loop from zero to the one minus the number of radio button selections
	for (counter = 0; counter < maxpmethods; counter++)
	{
		// If a radio button has been selected it will return true
		// (If not it will return false)
		if (frm.payment[counter].checked)
			paymentsel=frm.payment[counter].value;
	}
}
else
{
	if (frm.payment != 'undefined' && frm.payment != null)
		paymentsel=frm.payment.value;
}


 if (paymentsel>'')
  {
  	paymentinfo=paymentsel.split("-");
  
  
  	
    for (var i = 0; i<frm.elements.length; i++) {
        if ((frm.elements[i].name.indexOf('OPTREQ') > -1)) {
            if ((frm.elements[i].name.indexOf('ff'+paymentinfo[1]+'_') > -1)) {
            if (frm.elements[i].value <='')
            {alert ("Please fill in all required fields.");
            frm.elements[i].focus();         
            return false;
            }
        	}
        }
    }
  

   }
	
	if (CheckCreditCards()!=false) //' If credit cards pass, lets check submit wasnt done twice. 
	{
	if (checkreq_questions3()!=false) 
	{		
	return submitForm();
	}
	else
	{
	return false;
	}
	
	}
	else
	{
		return false;
	}
	
}

function CheckCreditCards()
{
	
	var comingFrom = "";
	
	if (arguments.length == 1)
	{
		comingFrom = arguments[0];
	}
	
	var frm = document.forms["billing"];
	var paymentsel;
	var maxpmethods=0;
  
	if (comingFrom == 'virtualterminal')
	{
		maxpmethods=1;
	}
	else
	{	
		if (frm.payment != 'undefined' && frm.payment != null)
			if (frm.payment.length!='undefined')  
				maxpmethods=frm.payment.length;
	}

	if (maxpmethods>0) 
	{
		// Loop from zero to the one minus the number of radio button selections
		for (counter = 0; counter < maxpmethods; counter++)
		{
			// If a radio button has been selected it will return true
			// (If not it will return false)
			if (comingFrom == 'virtualterminal')
			{
				paymentsel='online-'+frm.payment.value;
			}
			else
			{
				if (frm.payment[counter].checked)
					paymentsel=frm.payment[counter].value;
			}
		}
	}
	else
	{
		if (frm.payment != 'undefined' && frm.payment != null)
			paymentsel=frm.payment.value;
	}


	if (paymentsel > '')
	{
  		paymentinfo=paymentsel.split("-");

		//Check if credit card field is present, if so, check validity...
  		var cc_field
  		var paymentid=paymentinfo[1];
  		var cc_expmonth;
  		var cc_expyear;
  		var cc_cvv2;
  		var cc_type;
  		var ck_routing;
  		var ck_account;
  		var cc_cvv2_required;

		if (paymentsel.indexOf("CIM") > 1)
		{
			return true;	//Remove this in case we chage the cc selection from Dropdown to checkbox/radio...
			
			maxCIMProfiles = 0;
			if (frm.authCIMProfileID != 'undefined' && frm.authCIMProfileID != null)
				if (frm.authCIMProfileID.length)
					maxCIMProfiles=frm.authCIMProfileID.length;

			//alert(maxCIMProfiles);
			if (maxCIMProfiles > 0)
			{
				for (counter = 0; counter < maxCIMProfiles; counter++)
				{
					//alert(frm.authCIMProfileID[counter].value);
					if (frm.authCIMProfileID[counter].checked)
						return true;
				}
			}
			else
			{
				//alert(frm.authCIMProfileID.value);
				//alert(frm.authCIMProfileID.checked);
				if (frm.authCIMProfileID.checked)
					return true;
			}
			
			alert('Please select a credit card.');
			return false;
		}

  		if (comingFrom == 'virtualterminal')
  		{
  			cc_field=eval("document.forms['billing'].ocardno");
  			cc_expmonth=eval("document.forms['billing'].ocardexpiresmonth");
  			cc_expyear=eval("document.forms['billing'].ocardexpiresyear");
  			cc_cvv2=eval("document.forms['billing'].ocardcvv2");
  		}
  		else
  		{
  			cc_field=eval("document.forms['billing'].ff" + paymentid + "_ocardno");
  			cc_expmonth=eval("document.forms['billing'].ff" + paymentid + "_ocardexpiresmonth");
  			cc_expyear=eval("document.forms['billing'].ff" + paymentid + "_ocardexpiresyear");
  			cc_cvv2=eval("document.forms['billing'].ff" + paymentid + "_ocardcvv2");
			cc_cvv2_required=eval("document.forms['billing'].hdnCvvRequired");  	  	    
  			cc_type=eval("document.forms['billing'].ff" + paymentid + "_ocardtype");
  			ck_routing = eval("document.forms['billing'].ff" + paymentid + "_ocheckrouting");
  			ck_account = eval("document.forms['billing'].ff" + paymentid + "_ocheckaccount");
  		}  	

		if ((cc_cvv2!=undefined) && (cc_cvv2_required!=undefined)) 
		{
			if (cc_cvv2.value=="" && cc_cvv2_required.value=="1")
			{
				alert("Please enter CVV2 (Card Verification Code)");
  				return false;
			}
		}

  		if ((cc_field!=undefined) && (cc_expmonth!=undefined) && (cc_expyear!=undefined))
  		{
  			return CheckCardNumber(cc_field,cc_expmonth,cc_expyear,cc_type);
  		}
  		else
  		{
  			if ((ck_routing!=undefined) && (ck_account!=undefined))
  			{
				if (ck_routing.value.replace(/^\s+|\s+$/g,"") == "") 
				{
					alert("Please enter a Routing Number.");
					ck_routing.focus();
					return false;
				}
				if (ck_account.value.replace(/^\s+|\s+$/g,"") == "") 
				{
					alert("Please enter an Account Number.");
					ck_account.focus();
					return false;
				}			
  			}
  			else
  				return true;
  		}
	  	
	}
  
  
  
 // if(frm.pwd1.value != frm.pwd2.value)
 // {
  //  alert('The Password and verified password don not match!');
  //  return false;
 // }
 // else
  //{
  //  return true;
 // }
}

var Cards = new makeArray(8);
Cards[0] = new CardType("MasterCard", "51,52,53,54,55", "16");
var MasterCard = Cards[0];
Cards[1] = new CardType("VisaCard", "4", "13,16");
var VisaCard = Cards[1];
Cards[2] = new CardType("AmExCard", "34,37", "15");
var AmExCard = Cards[2];
Cards[3] = new CardType("DinersClubCard", "30,36,38", "14");
var DinersClubCard = Cards[3];
Cards[4] = new CardType("DiscoverCard", "6011", "16");
var DiscoverCard = Cards[4];
Cards[5] = new CardType("enRouteCard", "2014,2149", "15");
var enRouteCard = Cards[5];
Cards[6] = new CardType("JCBCard", "3088,3096,3112,3158,3337,3528", "16");
var JCBCard = Cards[6];
var LuhnCheckSum = Cards[7] = new CardType();

/*************************************************************************\
CheckCardNumber(form)
function called when users click the "check" button.
\*************************************************************************/
function CheckCardNumber(cardnum,cardmonth,cardyear,cc_type) {
var tmpyear;
if (cardnum.value.length == 0) {
alert("Please enter a Card Number.");
cardnum.focus();
return false;
}

if (cardyear.options[cardyear.selectedIndex].value > 2000)
tmpyear=cardyear.options[cardyear.selectedIndex].value;
else if (cardyear.options[cardyear.selectedIndex].value > 96)
tmpyear = "19" + cardyear.options[cardyear.selectedIndex].value;
else if (cardyear.options[cardyear.selectedIndex].value < 21)
tmpyear = "20" + cardyear.options[cardyear.selectedIndex].value;
else {                            
alert("The Expiration Year is not valid.");
return false;
}
tmpmonth = cardmonth.options[cardmonth.selectedIndex].value;


// The following line doesn't work in IE3, you need to change it
// to something like "(new CardType())...".
// if (!CardType().isExpiryDate(tmpyear, tmpmonth)) {
if (!(new CardType()).isExpiryDate(tmpyear, tmpmonth)) {
alert("This card has already expired.");
return false;
}

card = "MasterCard";

var retval = false;

if (cc_type == 'undefined' || cc_type == undefined)
{
	retval = new CardType().checkCardNumber(cardnum.value,tmpyear,tmpmonth,'');
}
else
{
	if(cc_type[cc_type.selectedIndex].value.toLowerCase() == 'maestro' && cardnum.value.length == 18)
	{
		retval = true;
	}
	else
	{
		retval = new CardType().checkCardNumber(cardnum.value,tmpyear,tmpmonth,cc_type.value);
	}
}
cardname = "";

if (retval){
	return true;}
else
{
	alert("Credit card number is incorrect");
	cardnum.focus();
	return false;}
}
/*************************************************************************\
Object CardType([String cardtype, String rules, String len, int year, 
                                        int month])
cardtype    : type of card, eg: MasterCard, Visa, etc.
rules       : rules of the cardnumber, eg: "4", "6011", "34,37".
len         : valid length of cardnumber, eg: "16,19", "13,16".
year        : year of expiry date.
month       : month of expiry date.
eg:
var VisaCard = new CardType("Visa", "4", "16");
var AmExCard = new CardType("AmEx", "34,37", "15");
\*************************************************************************/
function CardType() {
var n;
var argv = CardType.arguments;
var argc = CardType.arguments.length;

this.objname = "object CardType";

var tmpcardtype = (argc > 0) ? argv[0] : "CardObject";
var tmprules = (argc > 1) ? argv[1] : "0,1,2,3,4,5,6,7,8,9";
var tmplen = (argc > 2) ? argv[2] : "13,14,15,16,19";

this.setCardNumber = setCardNumber;  // set CardNumber method.
this.setCardType = setCardType;  // setCardType method.
this.setLen = setLen;  // setLen method.
this.setRules = setRules;  // setRules method.
this.setExpiryDate = setExpiryDate;  // setExpiryDate method.

this.setCardType(tmpcardtype);
this.setLen(tmplen);
this.setRules(tmprules);
if (argc > 4)
this.setExpiryDate(argv[3], argv[4]);

this.checkCardNumber = checkCardNumber;  // checkCardNumber method.
this.getExpiryDate = getExpiryDate;  // getExpiryDate method.
this.getCardType = getCardType;  // getCardType method.
this.isCardNumber = isCardNumber;  // isCardNumber method.
this.isExpiryDate = isExpiryDate;  // isExpiryDate method.
this.luhnCheck = luhnCheck;// luhnCheck method.
return this;
}

/*************************************************************************\
boolean checkCardNumber([String cardnumber, int year, int month])
return true if cardnumber pass the luhncheck and the expiry date is
valid, else return false.
\*************************************************************************/
function checkCardNumber() {
var argv = checkCardNumber.arguments;
var argc = checkCardNumber.arguments.length;
var cardnumber = (argc > 0) ? argv[0] : this.cardnumber;
var year = (argc > 1) ? argv[1] : this.year;
var month = (argc > 2) ? argv[2] : this.month;

this.setCardNumber(cardnumber);
this.setExpiryDate(year, month);

if (!this.isCardNumber())
return false;
if (!this.isExpiryDate())
return false;

return true;
}
/*************************************************************************\
String getCardType()
return the cardtype.
\*************************************************************************/
function getCardType() {
return this.cardtype;
}
/*************************************************************************\
String getExpiryDate()
return the expiry date.
\*************************************************************************/
function getExpiryDate() {
return this.month + "/" + this.year;
}
/*************************************************************************\
boolean isCardNumber([String cardnumber])
return true if cardnumber pass the luhncheck and the rules, else return
false.
\*************************************************************************/
function isCardNumber() {
var argv = isCardNumber.arguments;
var argc = isCardNumber.arguments.length;
var cardnumber = (argc > 0) ? argv[0] : this.cardnumber;
if (!this.luhnCheck())
return false;

for (var n = 0; n < this.len.size; n++)
if (cardnumber.toString().length == this.len[n]) {
for (var m = 0; m < this.rules.size; m++) {
var headdigit = cardnumber.substring(0, this.rules[m].toString().length);
if (headdigit == this.rules[m])
return true;
}
return false;
}
return false;
}

/*************************************************************************\
boolean isExpiryDate([int year, int month])
return true if the date is a valid expiry date,
else return false.
\*************************************************************************/
function isExpiryDate() {
var argv = isExpiryDate.arguments;
var argc = isExpiryDate.arguments.length;

year = argc > 0 ? argv[0] : this.year;
month = argc > 1 ? argv[1] : this.month;

if (!isNum(year+""))
return false;
if (!isNum(month+""))
return false;
today = new Date();
expiry = new Date(year, month);
if (today.getTime() > expiry.getTime())
return false;
else
return true;
}

/*************************************************************************\
boolean isNum(String argvalue)
return true if argvalue contains only numeric characters,
else return false.
\*************************************************************************/
function isNum(argvalue) {
argvalue = argvalue.toString();

if (argvalue.length == 0)
return false;

for (var n = 0; n < argvalue.length; n++)
if (argvalue.substring(n, n+1) < "0" || argvalue.substring(n, n+1) > "9")
return false;

return true;
}

/*************************************************************************\
boolean luhnCheck([String CardNumber])
return true if CardNumber pass the luhn check else return false.
Reference: http://www.ling.nwu.edu/~sburke/pub/luhn_lib.pl
\*************************************************************************/
function luhnCheck() {
var argv = luhnCheck.arguments;
var argc = luhnCheck.arguments.length;

var CardNumber = argc > 0 ? argv[0] : this.cardnumber;

if (! isNum(CardNumber)) {
return false;
  }

var no_digit = CardNumber.length;
var oddoeven = no_digit & 1;
var sum = 0;

for (var count = 0; count < no_digit; count++) {
var digit = parseInt(CardNumber.charAt(count));
if (!((count & 1) ^ oddoeven)) {
digit *= 2;
if (digit > 9)
digit -= 9;
}
sum += digit;
}
if (sum % 10 == 0)
return true;
else
return false;
}

/*************************************************************************\
ArrayObject makeArray(int size)
return the array object in the size specified.
\*************************************************************************/
function makeArray(size) {
this.size = size;
return this;
}

/*************************************************************************\
CardType setCardNumber(cardnumber)
return the CardType object.
\*************************************************************************/
function setCardNumber(cardnumber) {
this.cardnumber = cardnumber;
return this;
}

/*************************************************************************\
CardType setCardType(cardtype)
return the CardType object.
\*************************************************************************/
function setCardType(cardtype) {
this.cardtype = cardtype;
return this;
}

/*************************************************************************\
CardType setExpiryDate(year, month)
return the CardType object.
\*************************************************************************/
function setExpiryDate(year, month) {
this.year = year;
this.month = month;
return this;
}

/*************************************************************************\
CardType setLen(len)
return the CardType object.
\*************************************************************************/
function setLen(len) {
// Create the len array.
if (len.length == 0 || len == null)
len = "13,14,15,16,19";

var tmplen = len;
n = 1;
while (tmplen.indexOf(",") != -1) {
tmplen = tmplen.substring(tmplen.indexOf(",") + 1, tmplen.length);
n++;
}
this.len = new makeArray(n);
n = 0;
while (len.indexOf(",") != -1) {
var tmpstr = len.substring(0, len.indexOf(","));
this.len[n] = tmpstr;
len = len.substring(len.indexOf(",") + 1, len.length);
n++;
}
this.len[n] = len;
return this;
}

/*************************************************************************\
CardType setRules()
return the CardType object.
\*************************************************************************/
function setRules(rules) {
// Create the rules array.
if (rules.length == 0 || rules == null)
rules = "0,1,2,3,4,5,6,7,8,9";
  
var tmprules = rules;
n = 1;
while (tmprules.indexOf(",") != -1) {
tmprules = tmprules.substring(tmprules.indexOf(",") + 1, tmprules.length);
n++;
}
this.rules = new makeArray(n);
n = 0;
while (rules.indexOf(",") != -1) {
var tmpstr = rules.substring(0, rules.indexOf(","));
this.rules[n] = tmpstr;
rules = rules.substring(rules.indexOf(",") + 1, rules.length);
n++;
}
this.rules[n] = rules;
return this;
}
//  End -->



function getEl(elRef)
{
	if(typeof elRef=='string'){
		if(document.getElementById(elRef))return document.getElementById(elRef);
		if(document.forms[elRef])return document.forms[elRef];
		if(document[elRef])return document[elRef];
		if(window[elRef])return window[elRef];
	}
	return elRef;	// Return original ref.	
}

function getFamily(el,formRef)
{
	var els = formRef.elements;
	var retArray = new Array();
	for(var no=0;no<els.length;no++){
		if(els[no].name == el.name)retArray[retArray.length] = els[no];
	}
	return retArray;		
}

function getValuesAsArray(formRef)
{
	var retArray = new Object();
	formRef = getEl(formRef);
	var els = formRef.elements;
	for(var no=0;no<els.length;no++){
		if(els[no].disabled)continue;
		var tag = els[no].tagName.toLowerCase();
		switch(tag){
			case "input": 
				var type = els[no].type.toLowerCase();
				if(!type)type='text';
				switch(type){
					case "text":
					case "image":
					case "hidden":
					case "password":
						retArray[els[no].name] = els[no].value;
						break;
					case "checkbox":
						var boxes = this.getFamily(els[no],formRef);
						if(boxes.length>1){
							retArray[els[no].name] = new Array();
							for(var no2=0;no2<boxes.length;no2++){
								if(boxes[no2].checked){
									var index = retArray[els[no].name].length;
									retArray[els[no].name][index] = boxes[no2].value;
								}
							}								
						}else{
							if(els[no].checked)retArray[els[no].name] = els[no].value;
						}
						break;	
					case "radio":
						if(els[no].checked)retArray[els[no].name] = els[no].value;
						break;		
					
				}	
				break;	
			case "select":
				var string = '';			
				var mult = els[no].getAttribute('multiple');
				if(mult || mult===''){
					retArray[els[no].name] = new Array();
					for(var no2=0;no2<els[no].options.length;no2++){
						var index = retArray[els[no].name].length;
						if(els[no].options[no2].selected)retArray[els[no].name][index] = els[no].options[no2].value;	
					}
				}else{
					retArray[els[no].name] = els[no].options[els[no].selectedIndex].value;
				}
				break;	
			case "textarea":
				retArray[els[no].name] = els[no].value;
				break;					
		}			
	}
	return retArray;		
}

function isArray(el)
{
	if(el.constructor.toString().indexOf("Array") != -1)return true;
	return false;
}	

function popup(filename,width,height,scroll1)
{
	if (scroll1>0)
		result = window.open(filename, "popped", "width="+ width + ", height="+height+", location=no, menubar=no, status=no, toolbar=no, scrollbars=yes, resizable=no");
	else
		result = window.open(filename, "popped", "width="+ width + ", height="+height+", location=no, menubar=no, status=no, toolbar=no, scrollbars=no, resizable=no");
	
	if (result != null) 
		html = "is not blocking";
	else 
		alert("Your Browser is blocking popups which is preventing a 3dCart window to appear.");
} 