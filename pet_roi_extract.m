function out_csv = pet_roi_extract(pet_files, atlas_path, gm_mask_path, roi_list, out_csv)
% PET ROI extraction using SPM12
%
% Inputs:
%   pet_files    : MATLAB cell array of PET file paths
%   atlas_path   : atlas NIfTI file in MNI space
%   gm_mask_path : optional GM mask path, or '' if not used
%   roi_list     : numeric vector of ROI labels, [] to auto-detect
%   out_csv      : output CSV path
%
% Output:
%   out_csv      : saved CSV file path

    if nargin < 5
        error('Usage: pet_roi_extract(pet_files, atlas_path, gm_mask_path, roi_list, out_csv)');
    end

    % Initialize SPM
    spm('Defaults', 'PET');
    spm_jobman('initcfg');

    fprintf('Loading atlas: %s\n', atlas_path);
    V_atlas = spm_vol(atlas_path);
    atlas = spm_read_vols(V_atlas);

    % Detect ROI labels automatically if empty
    if isempty(roi_list)
        roi_list = unique(atlas(:));
        roi_list = roi_list(~isnan(roi_list));
        roi_list = roi_list(roi_list ~= 0);
        roi_list = sort(roi_list);
    else
        roi_list = roi_list(:)';
    end

    fprintf('Number of selected ROIs: %d\n', numel(roi_list));

    % Optional GM mask
    use_mask = false;
    gmask = [];
    if ~isempty(gm_mask_path)
        fprintf('Loading GM mask: %s\n', gm_mask_path);
        V_mask = spm_vol(gm_mask_path);
        gmask = spm_read_vols(V_mask);
        use_mask = true;
    end

    n_sub = numel(pet_files);
    n_roi = numel(roi_list);

    results = nan(n_sub, n_roi);
    subject_names = cell(n_sub, 1);

    % Basic dimension check
    atlas_size = size(atlas);

    if use_mask
        if ~isequal(size(gmask), atlas_size)
            error('GM mask dimensions do not match atlas dimensions.');
        end
    end

    for i = 1:n_sub
        pet_path = pet_files{i};

        if isempty(pet_path)
            continue;
        end

        [~, subj_name, ~] = fileparts(pet_path);
        subject_names{i} = subj_name;

        fprintf('Processing subject %d/%d: %s\n', i, n_sub, subj_name);

        V_pet = spm_vol(pet_path);
        img = spm_read_vols(V_pet);

        if ~isequal(size(img), atlas_size)
            error('PET image dimensions do not match atlas dimensions for subject: %s', subj_name);
        end

        if use_mask
            img = img .* gmask;
        end

        for j = 1:n_roi
            roi_val = roi_list(j);
            roi_mask = (atlas == roi_val);

            vals = img(roi_mask);

            if isempty(vals)
                results(i, j) = NaN;
            else
                results(i, j) = nanmean(vals);
            end
        end
    end

    % Create table
    var_names = cell(1, n_roi);
    for j = 1:n_roi
        var_names{j} = matlab.lang.makeValidName(sprintf('ROI_%d', roi_list(j)));
    end

    T = array2table(results, 'VariableNames', var_names);
    T = addvars(T, subject_names, 'Before', 1, 'NewVariableNames', 'Subject');

    writetable(T, out_csv);

    fprintf('ROI extraction completed.\n');
    fprintf('Saved CSV: %s\n', out_csv);
end