match (n) detach delete n;

create (_sem_label:`Sem_Label` {`description`:"the meta label to label labels", `techname`:"Sem_Label",`_uid`:"sem1",_schemaname:"Schema"})
create (_description:`Sem_Property` {`description`:"longer description", `scalartype`:"string", `techname`:"description",`_uid`:"sem2"})
create (_techname:`Sem_Property` {`description`:"internal scalar representation", `scalartype`:"string", `techname`:"techname",`_uid`:"sem3"})
create (_uid:`Sem_Property` {`description`:"a unique id", `scalartype`:"string", `techname`:"_uid",`_uid`:"sem4"})
create (_sem_prop:`Sem_Relation` {`description`:"Sem_Label --SEM_PROP-> Sem_Property", `techname`:"SEM_PROP",`_uid`:"sem5",_startschemas:[],_endschemas:[]})
create (_arity:`Sem_Property` {`description`:"How often can there be the element", `scalartype`:"string", `techname`:"arity",`_uid`:"sem7"})
create (_sem_relation:`Sem_Label` {`description`:"used to define a type of relation", `techname`:"Sem_Relation",`_uid`:"sem8", _schemaname:"Relation"})
create (_sem_property:`Sem_Label` {`description`:"A description of  property of semantic meta object", `techname`:"Sem_Property",`_uid`:"sem9", _schemaname:"Property"})
create (_fieldtype:`Sem_Property` {`description`:"Von welchem Typ ist der Wert", `scalartype`:"string", `techname`:"scalartype",`_uid`:"sem10"})
create (_name:`Sem_Property` {`description`:"full name of  thing",  `scalartype`:"string", `techname`:"name",`_uid`:"sem11"})
create (_person:`Sem_Label` {`description`:"a human", `techname`:"Person",`_uid`:"sem12", _schemaname:"Person"})
create (_firstname:`Sem_Property` {`description`:"first name of a person", `scalartype`:"string", `techname`:"firstname",`_uid`:"sem13"})
create (_lastname:`Sem_Property` {`description`:"last name of a person", `scalartype`:"string", `techname`:"lastname",`_uid`:"sem14"})
create (_likes:`Sem_Relation` {`description`:"xoxoxo", `techname`:"LIKES",`_uid`:"sem15",_startschemas:[],_endschemas:[]})
create (_bob:`Person` {`name`:"Bob",`_uid`:"sem16", `lastname`:"", `firstname`:""})
create (_alice:`Person` {`firstname`:"Alice", `lastname`:"Alison", `name`:"Alice Alison",`_uid`:"sem17"})
create (_schemaname:`Sem_Property` {`description`:"the name of a schema", `scalartype`:"string", `techname`:"_schemaname",`_uid`:"sem18"})
create (_startschemas:`Sem_Property` {`description`:"schemas of startnode", `scalartype`:"string", `techname`:"_startschemas",`_uid`:"sem19"})
create (_endschemas:`Sem_Property` {`description`:"schemas of endnode", `scalartype`:"string", `techname`:"_endschemas",`_uid`:"sem20"})


create (_sem_label)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem21"}]->(_description)
create (_sem_label)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem22"}]->(_techname)
create (_sem_label)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem23"}]->(_uid)
create (_sem_label)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem24"}]->(_schemaname)

create (_sem_prop)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem25"}]->(_arity)
create (_sem_prop)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem26"}]->(_uid)

create (_sem_relation)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem27"}]->(_techname)
create (_sem_relation)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem28"}]->(_description)
create (_sem_relation)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem29"}]->(_uid)
create (_sem_relation)-[:`SEM_PROP` {`arity`:"*",`_uid`:"sem30"}]->(_startschemas)
create (_sem_relation)-[:`SEM_PROP` {`arity`:"*",`_uid`:"sem31"}]->(_endschemas)

create (_sem_property)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem32"}]->(_fieldtype)
create (_sem_property)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem33"}]->(_description)
create (_sem_property)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem34"}]->(_techname)
create (_sem_property)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem35"}]->(_uid)

create (_person)-[:`SEM_PROP` {`arity`:"?",`_uid`:"sem36"}]->(_lastname)
create (_person)-[:`SEM_PROP` {`arity`:"?",`_uid`:"sem37"}]->(_firstname)
create (_person)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem38"}]->(_name)
create (_person)-[:`SEM_PROP` {`arity`:"1",`_uid`:"sem39"}]->(_uid)

create (_bob)-[:`LIKES`]->(_alice)
create (_alice)-[:`LIKES`]->(_bob)
;