# -*- coding: utf-8 -*-

import sys
import os
import platform
from pprint import pprint

import studio_globals
from atk_shotgun.ShotgunTankAccess import ShotgunTankAccess
from atk_global import atk_globals
import sgtk

reload(atk_globals)

class Custom_Query(object):
    """
    Class to wrap SG-Queries to manage more the expected return value.
    """

    def __init__(self):

        self.shotgun_access_obj = ShotgunTankAccess.Shotgun_Tank_Access()
        self.sg = self.shotgun_access_obj.get_sg()

    def get_all_users(self):
        """
        """
        fields = []
        filters = []
        users = []

        user_list = self.sg.find("HumanUser", filters, fields)

        for dict in user_list:
            users.append(dict)

        return users
    
    def get_all_projects(self, active=False):
        fields = ['name']
        if active:
            filters = [["sg_status", "is", "Active"]]
        else:
            filters = []
        project_list = self.sg.find("Project", filters, fields)
        return project_list

    def get_project_id_by_name(self, project_name):
        """
        """
        fields = ['id']
        filters = [["name", "is", project_name]]
        project = self.sg.find_one("Project", filters, fields)
        return project
    
    def get_sequence_id_by_name(self, project_id, sequence_name):
        """
        """
    
        filters = [
            ['project','is',{'type':'Project','id':project_id}],
            ['code', 'is', sequence_name]
            ]
        ## Get a list with _all shots of the sequence
        sequence_entity = ( self.sg.find_one('Sequence',filters) )  
        return sequence_entity  

    def get_entity_by_project_name(self, project_name):

        default_root_path = atk_globals.PROJECTS_DRIVE
        project_root_path = os.path.join(default_root_path, project_name)
        tk = sgtk.sgtk_from_path(project_root_path)
        result = tk.entity_from_path(project_root_path)
        return result

    def get_project_handles_by_project_name(self, project_name):
        """
        Return the project Cut-In
        """
        fields = ['sg_global_cutin', 'sg_global_cutout', 'sg_global_headin', 'sg_global_tailout']
        filters = [['name', 'is', project_name]]
        sg_entity_type = "Project"
        data = self.sg.find_one(sg_entity_type, filters=filters, fields=fields)
        return data

    def is_shot_anamorphic_by_id(self, shot_id):

        sg_entity_type = "Shot"
        sg_filters = [["id", "is", shot_id]]
        fields = ['sg_shot_anamorphic']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
                
        if data is None or data["sg_shot_anamorphic"] is None:
            return False
        else:
            return data["sg_shot_anamorphic"]

    def get_shot_aspect_ration_by_id(self, shot_id):

        sg_entity_type = "Shot"
        sg_filters = [["id", "is", shot_id]]
        fields = ['sg_aspect_ratio']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
                
        if data is None or data["sg_aspect_ratio"] is None:
            return False
        else:
            return data["sg_aspect_ratio"]
        
        
    def get_shot_pixel_aspect_ration_by_id(self, shot_id):

        sg_entity_type = "Shot"
        sg_filters = [["id", "is", shot_id]]
        fields = ['sg_shot_pixel_aspect_ratio']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
                
        if data is None or data["sg_shot_pixel_aspect_ratio"] is None:
            return False
        else:
            return data["sg_shot_pixel_aspect_ratio"]
        
    def get_shot_colorspace_by_id(self, shot_id):

        sg_entity_type = "Shot"
        sg_filters = [["id", "is", shot_id]]
        fields = ['sg_shot_colorspace']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
                
        if data is None or data["sg_shot_colorspace"] is None:
            return False
        else:
            return data["sg_shot_colorspace"]


    def get_shot_resolution_by_id(self, shot_id):

        sg_entity_type = "Shot"
        sg_filters = [["id", "is", shot_id]]
        fields = ['sg_resolution']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data is None or data["sg_resolution"] is None:
            return False
        else:
            return data["sg_resolution"]


    def get_shot_frame_range_by_shot_code(self, shot_code):
        """

        :param shot_code:
        :return:
        """

        sg_filters = [["code", "is", shot_code]]
        fields = ['sg_cut_in', 'sg_cut_out']
        data = self.sg.find_one("Shot", filters=sg_filters, fields=fields)

        if data is None or data["sg_cut_in"] is None or data["sg_cut_out"] is None:
            return False
        else:
            return int(data["sg_cut_in"]), int(data["sg_cut_out"])

    def get_all_tasks_by_shot_id(self, shot_id):
        """
        """
        fields = ["content"]
        filters = [['entity', 'is', {'type': 'Shot', 'id': shot_id}]]
        task_entites = (self.sg.find('Task', filters, fields))
        return task_entites

    def get_all_tasks_by_asset_id(self, asset_id):
        """
        """
        fields = ["content"]
        filters = [['entity', 'is', {'type': 'Asset', 'id': asset_id}]]
        task_entites = ( self.sg.find('Task', filters, fields) )
        return task_entites
    
    def get_all_versions_by_shot_id(self, shot_id):
        """
        Return a list auf SG-Version entities.
        Like: [{'code': '010_030_plate_bg_v001.####',
                'entity': {'id': 9926, 'name': '010_030', 'type': 'Shot'},
                'id': 55063,
                'published_files': [{'id': 112221,
                       'name': '010_030_plate_bg_v001.%04d.dpx',
                       'type': 'PublishedFile'}],...]
        """
        
        fields = ['published_files', 'code', 'entity', 'sg_path_to_movie', 'client_code']
        filters = [['entity', 'is', {'type':'Shot', 'id': shot_id}]]
        version_entites = ( self.sg.find('Version', filters, fields) )
        return version_entites
    

    def get_all_published_files_by_shot_id(self, shot_id):
        """
        Return a list auf SG-Version entities.
        Like: [{'code': '010_030_plate_bg_v001.####',
                'entity': {'id': 9926, 'name': '010_030', 'type': 'Shot'},
                'id': 55063,
                'published_files': [{'id': 112221,
                       'name': '010_030_plate_bg_v001.%04d.dpx',
                       'type': 'PublishedFile'}],...]
        """
        
        fields = ['published_file_type', 'code', 'entity', 'path']
        filters = [['entity', 'is', {'type':'Shot', 'id': shot_id}]]
        version_entites = ( self.sg.find('PublishedFile', filters, fields) )
        return version_entites
    
    
    def get_published_file_type_by_id(self, published_file_id):
        """
        """
        fields = ['sg_assets', 'code', 'sg_elements', 'sg_file_path']
        filters = [['id', 'is', published_file_id]]
        
        published_file_entity = (self.sg.find_one('PublishedFileType', filters, fields) )
        return published_file_entity

    def get_published_file_type_by_name(self, published_file_name):
        """
        Return one entity of type PublishedFileType which match of the its name.
        :param published_file_name: 
        :return: Dictionary object
        """
        fields = ['sg_assets', 'code', 'sg_elements', 'sg_file_path']
        filters = [['code', 'is', published_file_name]]

        published_file_entity = (self.sg.find_one('PublishedFileType', filters, fields))
        return published_file_entity
    
    
    def get_version_entity_by_id(self, version_id, fields = ['published_files', 'code', 'entity']):
        """
        """
        filters = [["id", "is", version_id]]
        version_entity = self.sg.find_one('Version', filters, fields)  
        return version_entity

    def get_user_tasks(self, artist_name):
        """
        """
        user_entity = self.sg.find("HumanUser", [["name", "is", artist_name]])
        fields = ['id', 'content', 'task_assignees', 'time_logs_sum']
        filters = [["task_assignees", "is", user_entity]]

        result = self.sg.find("Task", filters, fields)
        return result

    def get_time_logs_by_user(self, artist_name):
        """
        """
        user_entity = self.sg.find_one("HumanUser", [["name", "is", artist_name]])

        fields = ['user', 'project', 'date', 'duration']
        filters = [
            ["user", "is", {'type': 'HumanUser', 'id': user_entity['id']}]
        ]

        time_log_entity = self.sg.find("TimeLog", filters, fields)

        return time_log_entity

    def get_time_logs_by_users(self, list_user_entity):
        """
        """
        list_time_logs = []

        for user_entity in list_user_entity:
            fields = ['user', 'project', 'date', 'duration']
            filters = [
                ["user", "is", {'type': 'HumanUser', 'id': user_entity['id']}]
            ]
            time_log_entity = self.sg.find("TimeLog", filters, fields)
            list_time_logs.append(time_log_entity)

            return list_time_logs
        
    def get_all_sequences_by_project_id(self, project_id):
        fields = ['code']
        filters = [['project', 'is', {'type': 'Project', 'id': project_id}]]
        
        sequence_entity = self.sg.find("Sequence", filters, fields)
        return sequence_entity

    def get_all_episodes_by_project_id(self, project_id):
        fields = ['code']
        filters = [['project', 'is', {'type': 'Project', 'id': project_id}]]

        episode_entity = self.sg.find("Episode", filters, fields)
        return episode_entity
    
    def get_all_shots_by_project_id(self, project_id):
        """
        Return _all Shotgun shots of the given project id.
        @param project_id: Shotgun project id
        @type project_id: int
        @return: List of Shot entities.
        @type: List of dictionaries.
        """
        fields = ['code']
        filters = [['project', 'is', {'type': 'Project', 'id': project_id}]]
        shot_entites = self.sg.find("Shot", filters, fields)
        return shot_entites
    
    def get_all_shots_by_sequence_id(self, project_id, sequence_id):
        """
        Return _all Shotgun shots of the given sequence name.
        @param sequence_name: Shotgun sequence name
        @type sequence_name: String
        @return: List of Shot entities.
        @type: List of dictionaries.
        """
        fields = ["code"]
        filters = [
            ['project','is',{'type':'Project','id':project_id}],
            ['sg_sequence', 'is', {'type':'Sequence','id': sequence_id}]
            ]
        shot_entites = ( self.sg.find('Shot',filters, fields) )
        return shot_entites
    
    def get_shot_id_by_name(self, project_id, sequence_id, shot_name):
        """
        """
        fields = ['id']
        filters = [
            ['project','is',{'type':'Project','id':project_id}],
            ['sg_sequence', 'is', {'type':'Sequence','id': sequence_id}],
            ["code", "is", shot_name]
            ]
        shot_entity = self.sg.find_one('Shot', filters, fields)  
        return shot_entity

    def get_asset_id_by_name(self, project_id, sequence_id, asset_name):
        """
        """
        fields = ['id']
        filters = [
            ['project','is',{'type':'Project','id':project_id}],
            ["code", "is", asset_name]
            ]
        asset_entity = self.sg.find_one('Asset', filters, fields)
        return asset_entity
    

    def get_shot_entity_by_id(self, shot_id):
        """
        """
        fields = ['sg_sequence', 'code']
        filters = [
            ["id", "is", shot_id]
            ]
        shot_entity = self.sg.find_one('Shot', filters, fields)  
        return shot_entity

    def get_shot_entity_by_code(self, shot_code):
        """
        """
        fields = ['sg_sequence', 'code']
        filters = [
            ["code", "is", shot_code]
            ]
        shot_entity = self.sg.find_one('Shot', filters, fields)  
        return shot_entity

    def get_asset_entity_by_code(self, asset_code):
        """
        """
        fields = ['code']
        filters = [
            ["code", "is", asset_code]
            ]
        asset_entity = self.sg.find_one('Asset', filters, fields)
        return asset_entity
    
    def get_assets_entity_by_asset_type(self, sg_project_entity, asset_type):
        """
        Return ALL assets of the given asset type and project ID
        """
        fields = ['code']
        filters = [
            ['project', "is", sg_project_entity],
            ['sg_asset_type', "is", asset_type]
            ]
        
        assets_entity = self.sg.find('Asset', filters, fields)  
        return assets_entity

    def get_asset_entity_by_id(self, asset_id):
        """
        """
        fields = ['sg_asset_type', 'code']
        filters = [
            ["id", "is", asset_id]
            ]
        asset_entity = self.sg.find_one('Asset', filters, fields)  
        return asset_entity 


    def get_sequence_name_by_id(self, project_id, shot_id):
        shot_id = int(shot_id)
        fields = ['code']
        filters = [['project', 'is', {'type': 'Project', 'id': project_id}],
                   ['shots', 'is', {'type': 'Shot', 'id': shot_id}]
                   ]
        sequence_entity = self.sg.find_one("Sequence", filters, fields)
        return sequence_entity['code']

    def get_lut_entity_by_id(self, entity_id):
        """
        Return the Shot LUT entity
        """
        entity_id = int(entity_id)
        fields = ['sg_shot_lut_file', 'sg_grade', 'sg_process_space', 'sg_output_process_space']
        filters = [['id', 'is', entity_id]]
        shot_lut_entity_list = self.sg.find_one(studio_globals.ENTITY_LUT, filters, fields)
        if len(shot_lut_entity_list) > 0:
            return shot_lut_entity_list
        else:
            return None

    def get_lut_from_shotgun(self, sg_entity_type, sg_id):
        """
        Return the LUT entity of the assigned Shot-LUT of the Shotgun entity type.
        """
        sg_filters = [["id", "is", sg_id]]
        sg_profile_field = 'custom_entity24_sg_shot_custom_entity24s'
        fields = ['sg_lut', 'sg_lut_file', sg_profile_field]
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        result = data[sg_profile_field]
        try:
            if len(result) > 0:
                return result
            else:
                return None
        except:
            return None
        
    def get_project_lut_entity_by_id(self, entity_id):
        """
        Return the project LUT entity
        """
        entity_id = int(entity_id)
        fields = ['sg_project_lut_file', 'sg_output_process_space', 'sg_process_space']
        filters = [['id', 'is', entity_id]]
        lut_fpn = self.sg.find_one(studio_globals.PROJECT_ENTITY_LUT, filters, fields)
        return lut_fpn

    def get_project_diy_transcoding_by_id(self, project_id):
        """
        :param project_id:
        :return:
        """
        sg_entity_type = "Project"
        sg_filters = [["id", "is", project_id]]
        fields = ['sg_diy_transcoding']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_diy_transcoding"] == None:
            return False
        else:
            sg_diy_transcoding = data["sg_diy_transcoding"]
            return sg_diy_transcoding


    def get_project_diy_transcoding_by_name(self, project_name):
        """
        :param project_id:
        :return:
        """
        sg_entity_type = "Project"
        sg_filters = [["name", "is", project_name]]
        fields = ['sg_diy_transcoding']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_diy_transcoding"] == None:
            return False
        else:
            sg_diy_transcoding = data["sg_diy_transcoding"]
            return sg_diy_transcoding


    def get_project_lut_from_shotgun(self, sg_entity_type, sg_id):
        """
        Return the LUT entity of the assigned Project-LUT of the Shotgun project.
        """
        sg_id = int(sg_id)
        sg_field = "custom_non_project_entity24_sg_project_custom_non_project_entity24s"
        sg_filters = [["id", "is", sg_id]]
        fields = [sg_field]
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        if len(data[sg_field]) > 0:
            return (data[sg_field][0])
        else:
            return None
        
    def get_cc_lut_process_color_space_by_entity_id(self, entity_id):
        """
        """
        fields = ['sg_process_space']
        filters = [['id', 'is', entity_id]]
        data = self.sg.find_one(studio_globals.PROJECT_ENTITY_LUT, filters, fields)
        return (data["sg_process_space"]) 

    def get_cc_lut_output_process_color_space_by_entity_id(self, entity_id):
        """
        """
        fields = ['sg_output_process_space']
        filters = [['id', 'is', entity_id]]
        data = self.sg.find_one(studio_globals.PROJECT_ENTITY_LUT, filters, fields)
        return (data["sg_output_process_space"]) 

    def get_lut_process_color_space_by_entity_id(self, entity_id):
        """
        """
        fields = ['sg_process_space']
        filters = [['id', 'is', entity_id]]
        data = self.sg.find_one(studio_globals.ENTITY_LUT, filters, fields)
        return (data["sg_process_space"])
    
    def get_lut_output_process_color_space_by_entity_id(self, entity_id):
        """
        """
        fields = ['sg_output_process_space']
        filters = [['id', 'is', entity_id]]
        data = self.sg.find_one(studio_globals.ENTITY_LUT, filters, fields)
        return (data["sg_output_process_space"])
    
    def get_aspect_ratio_by_project_name(self, sg_project_name):
        fields = ['sg_aspect_ratio']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_aspect_ratio"]
        if result is None or result == 0:
            return 1.0
        else:
            return result
        
    def is_full_range_by_project_id(self, sg_project_id):
        fields = ['sg_dnxhr']
        filters = [['id', 'is', sg_project_id]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_dnxhr"]
        if result is None:
            return False
        else:
            return result
        
    def is_full_range_by_project_name(self, sg_project_name):
        fields = ['sg_dnxhr']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_dnxhr"]
        if result is None:
            return False
        else:
            return result
        
    def get_aspect_ratio_by_project_id(self, sg_project_id):
        fields = ['sg_aspect_ratio']
        filters = [['id', 'is', sg_project_id]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_aspect_ratio"]
        if result is None or result == 0:
            return 1.0
        else:
            return result
        
    def get_frame_rate_by_project_name(self, sg_project_name):
        fields = ['sg_fps']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_fps"]
        if result is None or result == 0:
            return 24
        else:
            return result
        

    def get_frame_rate_by_project_id(self, project_id):
        fields = ['sg_fps']
        filters = [['id', 'is', project_id]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_fps"]
        if result is None or result == 0:
            return 24
        else:
            return result

    def is_anamorphic_by_project_name(self, sg_project_name):
        fields = ['sg_anamorphic']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_anamorphic"]
        return result

    def is_anamorphic_by_project_id(self, sg_project_id):
        fields = ['sg_anamorphic']
        filters = [['id', 'is', sg_project_id]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_anamorphic"]
        return result  

    def get_colorspace_by_project_name(self, sg_project_name):
        fields = ['sg_colorspace']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_colorspace"]
        return result
    
    def get_colorspace_by_project_id(self, sg_project_id):
        fields = ['sg_colorspace']
        filters = [['id', 'is', sg_project_id]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_colorspace"]
        return result    

    def get_pixel_aspect_ratio_by_project_name(self, sg_project_name):
        fields = ['sg_pixel_ratio']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_pixel_ratio"]
        if result is None or result == 0:
            return 1.0
        else:
            return result
            
    def get_display_colorspace_by_project_name(self, sg_project_name):
        fields = ['sg_display_colorspace']
        filters = [['name', 'is', sg_project_name]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_display_colorspace"]
        if result is None or result == "":
            return 'sRGB'
        else:
            return result
            
    def get_display_colorspace_by_project_id(self, sg_project_id):
        fields = ['sg_display_colorspace']
        filters = [['id', 'is', sg_project_id]]
        result = self.sg.find_one("Project", filters, fields)
        result = result["sg_display_colorspace"]
        if result is None or result == "":
            return 'sRGB'
        else:
            return result
        
    def check_shotgun_project_name_by_name(self, project_name):
        fields = ['name']
        filters = [['name', 'is', project_name]]
        result = self.sg.find_one("Project", filters, fields)
        if result is None:
            return False
        else:
            return True
        
    def update_group_by_id(self, sg_id=18):
        """
        Update as default the group 'Pipeline News Letter'.
        The group will extend by user how are "Lead, Artist, Supervisor"
        as well the account is active.
        """
        filters = [
            ["sg_status_list", "is", "act"],
            {
                "filter_operator": "any",
                "filters": [
                            ["sg_role", "is", "Artist"],
                            ["sg_role", "is", "Lead"],
                            ["sg_role", "is", "Supervisor"]
                            ]
            }
        ]
        user_entitys = self.sg.find("HumanUser", filters)
        data = {'users': user_entitys}
        result = self.sg.update("Group", sg_id, data)
        return result

    def get_shotgun_assets(self):
        fields = []
        filters = []
        result = self.sg.find("Asset", filters, fields)
        return result

    def get_elements(self):
        """
        Return a list of ALL Shotgun Elements.
        @return: A list of _all Elements.
        @type: List of multiple dictionaries
        """
        fields = ['code', 'sg_file_path', 'sg_used_by_projects', 'sg_file_type', 'sg_element_type']
        filters = []
        sg_element = studio_globals.ELEMENT
        result = self.sg.find(sg_element, filters, fields)

        return result


    def get_element_by_name(self, element_name):
        """
        Return a list of ALL Shotgun Elements.
        @return: A list of _all Elements.
        @type: List of multiple dictionaries
        """
        sg_element = studio_globals.ELEMENT
        fields = ['code', 'id', 'sg_file_path', 'sg_type', 'sg_file_type']
        filters = [['code', 'is', element_name]]
        result = self.sg.find_one(sg_element, filters, fields)

        return result

    def get_element_by_id(self, element_id):
        """
        Return a list of ALL Shotgun Elements.
        @return: A list of _all Elements.
        @type: List of multiple dictionaries
        """
        sg_element = studio_globals.ELEMENT
        fields = ['code', 'id', 'sg_file_path', 'sg_type', 'sg_file_type']
        filters = [['id', 'is', element_id]]
        result = self.sg.find_one(sg_element, filters, fields)

        return result

    def get_versions_by_element_id(self, element_id):
        """
        Return a list of ALL Shotgun Elements.
        @return: A list of _all Elements.
        @type: List of multiple dictionaries
        """
        fields = ['code', 'sg_file_path', 'sg_used_by_projects', 'sg_file_type', 'sg_element_type']
        filters = []
        sg_element = studio_globals.ELEMENT
        filters = [['entity', 'is', {'type': sg_element, 'id': element_id}]]
        version_entites = ( self.sg.find('Version', filters, fields))
        return version_entites
    
    def get_elements_entity_by_element_type(self, element_type):
        """
        Return ALL Elements of the given Element type like 'Vehicle'.
        :param element_type: Name of the Element type.
        :type String
        :return: List of Dictionaries
        """

        fields = ['sg_type', 'code', 'sg_file_path', 'sg_file_type', 'sg_used_by_projects']
        filters = [
            ['sg_type', "is", element_type]
            ]
        
        elements_entity = self.sg.find(studio_globals.ELEMENT, filters, fields)
        return elements_entity
        
    def get_letterbox_opacity_by_project_id(self, project_id):
        """
        Return the 'Letterbox Opacity' value on project level otherwise 
        it will return as default 30, half transparent.
        @param project_id: Shotgun Project-ID
        @type project_id: Integer
        @return: Safety Crop value.
        @type: Integer
        """
        default_value = 30
        sg_entity_type = "Project"
        sg_filters = [["id", "is", project_id]]
        fields = ['sg_letterbox_opacity']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        
        if data["sg_letterbox_opacity"] == None:
            return default_value
        else:
            sg_letterbox_opacity = int(data["sg_letterbox_opacity"])
            return sg_letterbox_opacity
        
    def get_letterbox_opacity_by_project_name(self, project_name):
        """
        Return the 'Letterbox Opacity' value on project level otherwise 
        it will return as default 30, half transparent.
        @param project_id: Shotgun Project-Name
        @type project_id: Integer
        @return: Safety Crop value.
        @type: Integer
        """
        default_value = 30
        sg_entity_type = "Project"
        sg_filters = [["name", "is", project_name]]
        fields = ['sg_letterbox_opacity']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_letterbox_opacity"] == None:
            return default_value
        else:
            sg_letterbox_opacity = int(data["sg_letterbox_opacity"])
            return sg_letterbox_opacity
        
    def get_project_meta_data_by_id(self, project_id):
        """
        Return _all important information about the Shotgun project.
        @param project_id: Shotgun Project-ID
        @type project_id: Integer
        @return: 
        @type: dictionary
        """
        sg_entity_type = "Project"
        sg_filters = [["id", "is", project_id]]
        fields = ['sg_colorspace', 'sg_resolution', 'sg_pixel_ratio', 'sg_fps', 'sg_project_lut', 'sg_file_type']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        return data
    
    def get_aspect_ratio_from_project_resolution_by_id(self, project_id):
        """
        Return the aspect ratio from resolution field of the Shotgun project.
        @param project_id: Shotgun Project-ID
        @type project_id: Integer
        @return: 
        @type: float
        """
        sg_entity_type = "Project"
        sg_filters = [["id", "is", project_id]]
        fields = ['sg_resolution']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        if data:
            data = float(data["sg_resolution"].split(" ")[-1][:-2])
        return data
    
    def get_aspect_ratio_from_project_resolution_by_name(self, project_name):
        """
        Return the aspect ratio from resolution field of the Shotgun project.
        @param project_name: Shotgun Project-Name
        @type project_name: String
        @return: 
        @type: float
        """
        sg_entity_type = "Project"
        sg_filters = [["name", "is", project_name]]
        fields = ['sg_resolution']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        if data:
            data = float(data["sg_resolution"].split(" ")[-1][:-2])
        return data 
        
    def get_project_meta_data_by_name(self, project_name):
        """
        Return _all important information about the Shotgun project.
        @param project_name: Shotgun project name
        @type project_name: String
        @return: 
        @type: dictionary
        """
        sg_entity_type = "Project"
        sg_filters = [['name', 'is', project_name]]
        fields = ['sg_colorspace', 'sg_resolution', 'sg_pixel_ratio', 'sg_fps', 'sg_project_lut', 'sg_file_type']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        return data 
    
    def get_full_project_name_by_name(self, project_name):
        """
        Return the full project name.
        @param project_name: Shotgun project name
        @type project_name: String
        @return: 
        @type: dictionary
        """
        sg_entity_type = "Project"
        sg_filters = [['name', 'is', project_name]]
        fields = ['sg_full_project_name']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        return data
        
    
    def update_sg_entity(self, sg_entity_type, sg_id, update_data):
        """
        Update the Shotgun entity object with the given data.
        @param sg_entity_type: Shotgun entity
        @type sg_entity_type: String
        @param sg_id: Internal Shotgun ID of the specific entity object
        @type sg_id: Integer
        @param update_data: Addtional data for update
        @type update_data: dict
        @return: Updated SG entity object
        @type: dict
        """
        
        result = self.sg.update(sg_entity_type, sg_id, update_data)
        return result
        
    def get_draft_rate_by_project_name(self, project_name):
        """
        Return the 'Draft kbitRate Compression' value on project level.
        @param project_name: Shotgun Project-Name
        @type project_name: String
        @return: Integer value like 15000
        @type: None or Integer
        """
        sg_entity_type = "Project"
        sg_filters = [["name", "is", project_name]]
        fields = ['sg_draft_compression']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_draft_compression"] == None:
            return None
        else:
            sg_safety_crop_active = data["sg_draft_compression"]
            return sg_safety_crop_active
        
    def get_draft_rate_by_project_id(self, project_id):
        """
        Return the 'Draft kbitRate Compression' value on project level.
        @param project_id: Shotgun Project-ID
        @type project_name: Integer
        @return: Integer value like 15000
        @type: None or Integer
        """
        sg_entity_type = "Project"
        sg_filters = [["id", "is", project_id]]
        fields = ['sg_draft_compression']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_draft_compression"] == None:
            return None
        else:
            sg_safety_crop_active = data["sg_draft_compression"]
            return sg_safety_crop_active
        
        
    def get_protect_area_by_project_name(self, project_name):
        """
        Return the 'Protected Area' value on project level.
        @param project_name: Shotgun Project-Name
        @type project_name: String
        @return: String value like "2048x858"
        @type: None or String
        """
        sg_entity_type = "Project"
        sg_filters = [["name", "is", project_name]]
        fields = ['sg_protect_area']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_protect_area"] == None:
            return None
        else:
            sg_protected_area = data["sg_protect_area"]
            return sg_protected_area

    def get_focal_length_by_shot_id(self, shot_id):

        sg_entity_type = "Shot"
        sg_filters = [["id", "is", shot_id]]
        fields = ['sg_focal_length']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data == None or data["sg_focal_length"] == None:
            return None
        else:
            return data["sg_focal_length"]
        
    def get_default_tc_by_project_name(self, project_name):
        
        sg_entity_type = "Project"
        sg_filters = [["name", "is", project_name]]
        fields = ['sg_default_tc_start']
        data = self.sg.find_one(sg_entity_type, filters=sg_filters, fields=fields)

        if data["sg_default_tc_start"] == None:
            return "00:01:00:00"
        else:
            sg_default_tc_start = data["sg_default_tc_start"]
            return sg_default_tc_start

    def get_published_file_types(self):

        fields = ['code', 'sg_assets', 'sg_elements', 'short_name']
        filters = []

        publish_file_types = self.sg.find("PublishedFileType", filters, fields)
        return publish_file_types

    def get_sg_username_by_atk_username(self):
        """
        Helper function to match the ATK-Domain login
        username to the SG-Username.
        :return:
        """
        username = os.environ.get("USERNAME") or os.environ.get("USER")
        result = self.get_sg_user(username)

        if result != None:
            username = result['login']

        return username

    def get_sg_user(self, login_name):
        """
        :param login_name: 
        :return: 
        """

        filters = [["sg_atk_domain_login", "is", login_name]]
        fields = ['login', 'firstname', 'lastname', 'id', 'type']
        user_entity = self.sg.find_one("HumanUser", filters, fields)
        return user_entity

    def get_pipeline_step(self, step_name, entity_type_name):

        sg_filters = [
            ['code', 'is', step_name],
            ['entity_type', 'is', entity_type_name]
        ]
        fields = ['code', 'short_name', 'entity_type']
        pipleline_steps_entities = self.sg.find("Step", sg_filters, fields)

        return pipleline_steps_entities

    def get_pipeline_step_by_short_name(self, short_name, entity_type_name):

        sg_filters = [
            ['short_name', 'is', short_name],
            ['entity_type', 'is', entity_type_name]
        ]
        fields = ['code', 'short_name', 'code', 'entity_type']
        pipleline_steps_entity = self.sg.find_one("Step", sg_filters, fields)

        return pipleline_steps_entity

    def get_latest_publish(self, step_name, entity_type_name, asset_shot_code):
        """

        :param step_name:
        :param entity_type_name:
        :param asset_shot_code:
        :return:
        """

        if entity_type_name == "Shot":
            entity = self.get_shot_entity_by_code(asset_shot_code)
            tasks = self.get_all_tasks_by_shot_id(entity['id'])

        elif entity_type_name is "Asset":
            entity = self.get_asset_entity_by_code(asset_shot_code)
            tasks = self.get_all_tasks_by_asset_id(entity['id'])
        else:
            return

        for task in tasks:
            if task['content'] == step_name:
                task_entity = task

        sg_filters = [["code", "contains", asset_shot_code],
                      ['task', 'is', task_entity]
                      ]

        fields = ['path', 'name', 'published_file_type', 'task', 'version_number']
        data = self.sg.find("PublishedFile", sg_filters, fields)

        version_number_counter = 1
        temp_published_version = None

        for entry in data:
            if entry['version_number'] > version_number_counter:
                temp_published_version = entry
                version_number_counter = entry['version_number']

        return temp_published_version

    def get_latest_maya_scene_publish(self, step_name, entity_type_name, asset_shot_code):
        """
        Returns a dict with the latest SG-Published File based on the given parameter:
        :param step_name: Name of Pipeline Step, e.g: Animation, FX etc.
        :param entity_type_name: Like "Shot" or "Asset"
        :param asset_shot_code: Pure Shot-Code or Asset-Name/Code
        :return: Dictionary of the last Published File
        """

        if entity_type_name == "Shot":
            entity = self.get_shot_entity_by_code(asset_shot_code)
            tasks = self.get_all_tasks_by_shot_id(entity['id'])
        elif entity_type_name is "Asset":
            entity = self.get_asset_entity_by_code(asset_shot_code)
            tasks = self.get_all_tasks_by_asset_id(entity['id'])
        else:
            return

        for task in tasks:
            if task['content'] == step_name:
                task_entity = task

        sg_filters = [["code", "contains", asset_shot_code],
                      ['task', 'is', task_entity],
                      ['published_file_type', 'is', {'type': 'PublishedFileType', 'id': 3}]]

        fields = ['path', 'name', 'published_file_type', 'task', 'version_number']
        data = self.sg.find("PublishedFile", sg_filters, fields)

        version_number_counter = 0
        temp_published_version = None

        for entry in data:
            if entry['version_number'] > version_number_counter:
                temp_published_version = entry
                version_number_counter = entry['version_number']

        return temp_published_version
