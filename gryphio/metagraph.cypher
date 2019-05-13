match (n) detach delete n;

create (_label:`_Schema` {`description`:"the meta schema to label schemas", `techname`:"_Schema",`_uid`:"m1",_schemaname:"Schema"})
create (_description:`_Property` {`description`:"longer description", `scalartype`:"string", `techname`:"description",`_uid`:"m2"})
create (_techname:`_Property` {`description`:"internal scalar representation", `scalartype`:"string", `techname`:"techname",`_uid`:"m3"})
create (_uid:`_Property` {`description`:"a unique id", `scalartype`:"string", `techname`:"_uid",`_uid`:"m4"})
create (_prop:`_Relation` {`description`:"_Schema --_PROP-> _Property", `techname`:"_PROP",`_uid`:"m5",_startschemas:[],_endschemas:[]})
create (_arity:`_Property` {`description`:"How often can there be the element", `scalartype`:"string", `techname`:"arity",`_uid`:"m7"})
create (_relation:`_Schema` {`description`:"used to define a type of relation", `techname`:"_Relation",`_uid`:"m8", _schemaname:"Relation"})
create (_property:`_Schema` {`description`:"A description of  property of semantic meta object", `techname`:"_Property",`_uid`:"m9", _schemaname:"Property"})
create (_scalartype:`_Property` {`description`:"Von welchem Typ ist der Wert", `scalartype`:"string", `techname`:"scalartype",`_uid`:"m10"})
create (_name:`_Property` {`description`:"full name of  thing",  `scalartype`:"string", `techname`:"name",`_uid`:"m11"})
create (_person:`_Schema` {`description`:"a human", `techname`:"Person",`_uid`:"m12", _schemaname:"Person"})
create (_firstname:`_Property` {`description`:"first name of a person", `scalartype`:"string", `techname`:"firstname",`_uid`:"m13"})
create (_lastname:`_Property` {`description`:"last name of a person", `scalartype`:"string", `techname`:"lastname",`_uid`:"m14"})
create (_likes:`_Relation` {`description`:"xoxoxo", `techname`:"LIKES",`_uid`:"m15",_startschemas:[],_endschemas:[]})
create (_bob:`Person` {`name`:"Bob",`_uid`:"m16", `lastname`:"", `firstname`:""})
create (_alice:`Person` {`firstname`:"Alice", `lastname`:"Alison", `name`:"Alice Alison",`_uid`:"m17"})
create (_schemaname:`_Property` {`description`:"the name of a schema", `scalartype`:"string", `techname`:"_schemaname",`_uid`:"m18"})
create (_startschemas:`_Property` {`description`:"schemas of startnode", `scalartype`:"string", `techname`:"_startschemas",`_uid`:"m19"})
create (_endschemas:`_Property` {`description`:"schemas of endnode", `scalartype`:"string", `techname`:"_endschemas",`_uid`:"m20"})


create (_label)-[:`_PROP` {`arity`:"1",`_uid`:"m21"}]->(_description)
create (_label)-[:`_PROP` {`arity`:"1",`_uid`:"m22"}]->(_techname)
create (_label)-[:`_PROP` {`arity`:"1",`_uid`:"m23"}]->(_uid)
create (_label)-[:`_PROP` {`arity`:"1",`_uid`:"m24"}]->(_schemaname)

create (_prop)-[:`_PROP` {`arity`:"1",`_uid`:"m25"}]->(_arity)
create (_prop)-[:`_PROP` {`arity`:"1",`_uid`:"m26"}]->(_uid)

create (_relation)-[:`_PROP` {`arity`:"1",`_uid`:"m27"}]->(_techname)
create (_relation)-[:`_PROP` {`arity`:"1",`_uid`:"m28"}]->(_description)
create (_relation)-[:`_PROP` {`arity`:"1",`_uid`:"m29"}]->(_uid)
create (_relation)-[:`_PROP` {`arity`:"*",`_uid`:"m30"}]->(_startschemas)
create (_relation)-[:`_PROP` {`arity`:"*",`_uid`:"m31"}]->(_endschemas)

create (_property)-[:`_PROP` {`arity`:"1",`_uid`:"m32"}]->(_scalartype)
create (_property)-[:`_PROP` {`arity`:"1",`_uid`:"m33"}]->(_description)
create (_property)-[:`_PROP` {`arity`:"1",`_uid`:"m34"}]->(_techname)
create (_property)-[:`_PROP` {`arity`:"1",`_uid`:"m35"}]->(_uid)

create (_person)-[:`_PROP` {`arity`:"?",`_uid`:"m36"}]->(_lastname)
create (_person)-[:`_PROP` {`arity`:"?",`_uid`:"m37"}]->(_firstname)
create (_person)-[:`_PROP` {`arity`:"1",`_uid`:"m38"}]->(_name)
create (_person)-[:`_PROP` {`arity`:"1",`_uid`:"m39"}]->(_uid)

create (_bob)-[:`LIKES`]->(_alice)
create (_alice)-[:`LIKES`]->(_bob)
;